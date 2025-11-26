# app.py

import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, timedelta
import pandas as pd
from fpdf import FPDF

# ==============================
# Database Setup
# ==============================
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                subject TEXT,
                duration INTEGER,
                instructions TEXT,
                created_by TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                question TEXT,
                qtype TEXT,
                options TEXT,
                answer TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                user_id INTEGER,
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

def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def create_user(username, email, password, role):
    try:
        c.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                  (username, email, hash_password(password), role))
        conn.commit()
        return True
    except:
        return False

def create_quiz(title, subject, duration, instructions, created_by):
    c.execute("INSERT INTO quizzes (title, subject, duration, instructions, created_by) VALUES (?, ?, ?, ?, ?)",
              (title, subject, duration, instructions, created_by))
    conn.commit()

def add_question(quiz_id, question, qtype, options, answer):
    c.execute("INSERT INTO questions (quiz_id, question, qtype, options, answer) VALUES (?, ?, ?, ?, ?)",
              (quiz_id, question, qtype, options, answer))
    conn.commit()

def get_quizzes():
    c.execute("SELECT * FROM quizzes")
    return c.fetchall()

def get_questions(quiz_id):
    c.execute("SELECT * FROM questions WHERE quiz_id=?", (quiz_id,))
    return c.fetchall()

def record_attempt(quiz_id, user_id, start_time, end_time, score, answers):
    c.execute("INSERT INTO attempts (quiz_id, user_id, start_time, end_time, score, answers) VALUES (?, ?, ?, ?, ?, ?)",
              (quiz_id, user_id, start_time, end_time, score, str(answers)))
    conn.commit()

def generate_certificate(username, quiz_title, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Certificate of Completion", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"This certifies that {username} has completed the quiz '{quiz_title}'", 0, 1, 'C')
    pdf.cell(0, 10, f"Score Achieved: {score}", 0, 1, 'C')
    filename = f"{username}_{quiz_title}_certificate.pdf"
    pdf.output(filename)
    return filename

# ==============================
# Streamlit App
# ==============================
st.title("Online Quiz & Exam Management System")

# -------------------------
# Sidebar Navigation
# -------------------------
menu = ["Home", "Login", "Register"]
st.sidebar.title("Menu")
choice = st.sidebar.selectbox("Navigate", menu)

# -------------------------
# Registration Page
# -------------------------
if choice == "Register":
    st.subheader("Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')
    role = st.selectbox("Role", ["student", "teacher", "admin"])
    
    if st.button("Register"):
        if create_user(username, email, password, role):
            st.success("Account created successfully")
        else:
            st.error("Username or Email already exists")

# -------------------------
# Login Page
# -------------------------
elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user = get_user(username)
        if user and verify_password(password, user[3]):
            st.success(f"Logged in as {user[1]} ({user[4]})")
            st.session_state['user'] = user
        else:
            st.error("Invalid username or password")

# -------------------------
# Home / Dashboard
# -------------------------
elif choice == "Home":
    st.subheader("Welcome to Online Quiz System")
    if 'user' in st.session_state:
        user = st.session_state['user']
        st.write(f"Logged in as: {user[1]} ({user[4]})")

        # Admin/Teacher: Quiz Management
        if user[4] in ["teacher", "admin"]:
            st.subheader("Create a New Quiz")
            title = st.text_input("Quiz Title")
            subject = st.text_input("Subject")
            duration = st.number_input("Duration (minutes)", 1, 180)
            instructions = st.text_area("Instructions")
            
            if st.button("Create Quiz"):
                create_quiz(title, subject, duration, instructions, user[1])
                st.success("Quiz created successfully")
            
            st.subheader("Add Questions to Quiz")
            quizzes = get_quizzes()
            quiz_options = {q[1]: q[0] for q in quizzes}
            quiz_selected = st.selectbox("Select Quiz", list(quiz_options.keys()))
            
            question_text = st.text_area("Question Text")
            qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer", "Fill in the blanks"])
            options_text = st.text_area("Options (comma separated for MCQ)")
            answer_text = st.text_input("Answer")
            
            if st.button("Add Question"):
                add_question(quiz_options[quiz_selected], question_text, qtype, options_text, answer_text)
                st.success("Question added successfully")

        # Students: Take Quiz
        if user[4] == "student":
            st.subheader("Available Quizzes")
            quizzes = get_quizzes()
            for q in quizzes:
                st.write(f"**{q[1]}** | Subject: {q[2]} | Duration: {q[3]} mins")
                if st.button(f"Take Quiz: {q[1]}", key=f"take_{q[0]}"):
                    questions = get_questions(q[0])
                    answers = {}
                    start_time = datetime.now()
                    st.write(f"Quiz Started at {start_time.strftime('%H:%M:%S')}")
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
                    if st.button("Submit Quiz", key=f"submit_{q[0]}"):
                        score = 0
                        for ques in questions:
                            if ques[3] in ["MCQ", "True/False"] and answers[ques[0]] == ques[5]:
                                score += 1
                        end_time = datetime.now()
                        record_attempt(q[0], user[0], start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                       end_time.strftime('%Y-%m-%d %H:%M:%S'), score, answers)
                        st.success(f"Quiz submitted! Your score: {score}")
                        cert_file = generate_certificate(user[1], q[1], score)
                        st.download_button("Download Certificate", cert_file)
    else:
        st.info("Please login or register to use the system.")
