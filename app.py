# app.py

import streamlit as st
import sqlite3
from datetime import datetime
from fpdf import FPDF
import hashlib
import random
import string

# ==============================
# Database Setup
# ==============================
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

# Users table (admin, teachers)
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )''')

# Quizzes table
c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                subject TEXT,
                duration INTEGER,
                instructions TEXT,
                teacher_id INTEGER,
                link TEXT
            )''')

# Questions table
c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                question TEXT,
                qtype TEXT,
                options TEXT,
                answer TEXT
            )''')

# Submissions table
c.execute('''CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                student_name TEXT,
                roll_number TEXT,
                start_time TEXT,
                end_time TEXT,
                score REAL,
                answers TEXT
            )''')
conn.commit()

# ==============================
# Utility Functions
# ==============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

def create_user(username, password, role):
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                  (username.strip(), hash_password(password.strip()), role.strip().lower()))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    username = username.strip()
    password = password.strip()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user and verify_password(password, user[2]):
        return user
    return None

def create_quiz(title, subject, duration, instructions, teacher_id):
    link = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    c.execute("INSERT INTO quizzes (title, subject, duration, instructions, teacher_id, link) VALUES (?, ?, ?, ?, ?, ?)",
              (title, subject, duration, instructions, teacher_id, link))
    conn.commit()
    return link

def add_question(quiz_id, question, qtype, options, answer):
    c.execute("INSERT INTO questions (quiz_id, question, qtype, options, answer) VALUES (?, ?, ?, ?, ?)",
              (quiz_id, question, qtype, options, answer))
    conn.commit()

def get_teacher_quizzes(teacher_id):
    c.execute("SELECT * FROM quizzes WHERE teacher_id=?", (teacher_id,))
    return c.fetchall()

def get_quiz_by_link(link):
    c.execute("SELECT * FROM quizzes WHERE link=?", (link.strip(),))
    return c.fetchone()

def get_questions(quiz_id):
    c.execute("SELECT * FROM questions WHERE quiz_id=?", (quiz_id,))
    return c.fetchall()

def record_submission(quiz_id, student_name, roll_number, start_time, end_time, score, answers):
    c.execute("INSERT INTO submissions (quiz_id, student_name, roll_number, start_time, end_time, score, answers) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (quiz_id, student_name, roll_number, start_time, end_time, score, str(answers)))
    conn.commit()

def generate_certificate(student_name, quiz_title, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Certificate of Completion", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"This certifies that {student_name} has completed the quiz '{quiz_title}'", 0, 1, 'C')
    pdf.cell(0, 10, f"Score Achieved: {score}", 0, 1, 'C')
    filename = f"{student_name}_{quiz_title}_certificate.pdf"
    pdf.output(filename)
    return filename

# ==============================
# Streamlit App
# ==============================
st.title("Online Quiz & Exam System")

menu = ["Home", "Admin", "Teacher"]
choice = st.sidebar.selectbox("Menu", menu)

# ==========================
# Admin Section
# ==========================
if choice == "Admin":
    st.subheader("Admin Panel - Register Teacher")
    username = st.text_input("Teacher Username")
    password = st.text_input("Password", type='password')
    if st.button("Register Teacher"):
        if create_user(username, password, "teacher"):
            st.success(f"Teacher '{username}' registered successfully!")
        else:
            st.error("Username already exists!")

# ==========================
# Teacher Section
# ==========================
elif choice == "Teacher":
    st.subheader("Teacher Login")
    if 'teacher' not in st.session_state:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            user = login_user(username, password)
            if user and user[3].strip().lower() == "teacher":
                st.success(f"Logged in as {username}")
                st.session_state['teacher'] = user
            else:
                st.error("Invalid credentials or not a teacher")
    else:
        user = st.session_state['teacher']
        st.write(f"Welcome, {user[1]}!")

        # Create Quiz
        st.markdown("### Create Quiz")
        title = st.text_input("Quiz Title", key="quiz_title")
        subject = st.text_input("Subject", key="quiz_subject")
        duration = st.number_input("Duration (minutes)", 1, 180, key="quiz_duration")
        instructions = st.text_area("Instructions", key="quiz_instructions")
        if st.button("Create Quiz"):
            link = create_quiz(title, subject, duration, instructions, user[0])
            st.success(f"Quiz created! Share this link with students: **{link}**")

        # Add Questions
        quizzes = get_teacher_quizzes(user[0])
        if quizzes:
            quiz_options = {q[1]: q[0] for q in quizzes}
            selected_quiz_name = st.selectbox("Select Quiz to Add Questions", list(quiz_options.keys()))
            selected_quiz_id = quiz_options[selected_quiz_name]
            question_text = st.text_area("Question")
            qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer", "Fill in the blanks"])
            options_text = st.text_area("Options (comma separated for MCQ)")
            answer_text = st.text_input("Answer")
            if st.button("Add Question"):
                add_question(selected_quiz_id, question_text, qtype, options_text, answer_text)
                st.success("Question added successfully!")

        # View Submissions
        st.markdown("### View Submissions")
        for q in quizzes:
            st.write(f"Quiz: {q[1]} (Link: {q[6]})")
            c.execute("SELECT student_name, roll_number, score, answers FROM submissions WHERE quiz_id=?", (q[0],))
            submissions = c.fetchall()
            if submissions:
                for s in submissions:
                    st.write(f"Student: {s[0]} | Roll: {s[1]} | Score: {s[2]} | Answers: {s[3]}")
            else:
                st.write("No submissions yet.")

# ==========================
# Student Section
# ==========================
elif choice == "Home":
    st.subheader("Take Quiz via Link")
    quiz_link = st.text_input("Enter Quiz Link")
    if quiz_link:
        quiz = get_quiz_by_link(quiz_link)
        if quiz:
            st.write(f"Quiz: {quiz[1]} | Subject: {quiz[2]} | Duration: {quiz[3]} mins")
            student_name = st.text_input("Your Name", key="sname")
            roll_number = st.text_input("Your Roll Number", key="sroll")
            questions = get_questions(quiz[0])
            answers = {}
            for i, ques in enumerate(questions):
                st.write(f"Q{i+1}: {ques[2]}")
                if ques[3] == "MCQ":
                    opts = ques[4].split(",")
                    ans = st.radio("Select an option", opts, key=f"{ques[0]}")
                    answers[ques[0]] = ans
                elif ques[3] == "True/False":
                    ans = st.radio("Select True/False", ["True", "False"], key=f"{ques[0]}")
                    answers[ques[0]] = ans
                else:
                    ans = st.text_input("Answer", key=f"{ques[0]}")
                    answers[ques[0]] = ans
            if st.button("Submit Quiz"):
                score = 0
                for ques in questions:
                    if ques[3] in ["MCQ", "True/False"] and answers[ques[0]] == ques[5]:
                        score += 1
                start_time = datetime.now()
                record_submission(quiz[0], student_name, roll_number, start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), score, answers)
                st.success(f"Quiz submitted! Your score: {score}")
                cert_file = generate_certificate(student_name, quiz[1], score)
                st.download_button("Download Certificate", cert_file)
        else:
            st.error("Invalid quiz link!")
