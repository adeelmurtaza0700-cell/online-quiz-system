# app.py

import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from fpdf import FPDF

# ==============================
# Database Setup
# ==============================
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                subject TEXT,
                duration INTEGER,
                instructions TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                question TEXT,
                qtype TEXT,
                options TEXT,
                answer TEXT
            )''')

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
def create_quiz(title, subject, duration, instructions):
    c.execute("INSERT INTO quizzes (title, subject, duration, instructions) VALUES (?, ?, ?, ?)",
              (title, subject, duration, instructions))
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

menu = ["Home", "Teacher"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------------
# Teacher Section
# -------------------------
if choice == "Teacher":
    st.subheader("Teacher Dashboard")
    
    st.markdown("### Create Quiz")
    title = st.text_input("Quiz Title")
    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", 1, 180)
    instructions = st.text_area("Instructions")
    
    if st.button("Create Quiz"):
        create_quiz(title, subject, duration, instructions)
        st.success("Quiz created successfully!")
    
    st.markdown("### Add Questions")
    quizzes = get_quizzes()
    if quizzes:
        quiz_options = {q[1]: q[0] for q in quizzes}
        selected_quiz = st.selectbox("Select Quiz", list(quiz_options.keys()))
        question_text = st.text_area("Question")
        qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer", "Fill in the blanks"])
        options_text = st.text_area("Options (comma separated for MCQ)")
        answer_text = st.text_input("Answer")
        
        if st.button("Add Question"):
            add_question(quiz_options[selected_quiz], question_text, qtype, options_text, answer_text)
            st.success("Question added successfully!")
    
    st.markdown("### View Submissions")
    for q in quizzes:
        st.write(f"Quiz: {q[1]}")
        c.execute("SELECT student_name, roll_number, score, answers FROM submissions WHERE quiz_id=?", (q[0],))
        submissions = c.fetchall()
        if submissions:
            for s in submissions:
                st.write(f"Student: {s[0]} | Roll: {s[1]} | Score: {s[2]} | Answers: {s[3]}")
        else:
            st.write("No submissions yet.")

# -------------------------
# Student Section
# -------------------------
elif choice == "Home":
    st.subheader("Available Quizzes")
    quizzes = get_quizzes()
    for q in quizzes:
        st.write(f"**{q[1]}** | Subject: {q[2]} | Duration: {q[3]} minutes")
        if st.button(f"Take Quiz: {q[1]}", key=f"quiz_{q[0]}"):
            st.session_state['current_quiz'] = q[0]
            st.session_state['quiz_start'] = datetime.now()
    
    if 'current_quiz' in st.session_state:
        quiz_id = st.session_state['current_quiz']
        start_time = st.session_state['quiz_start']
        quiz = [q for q in quizzes if q[0] == quiz_id][0]
        st.write(f"Quiz: {quiz[1]} | Duration: {quiz[3]} minutes")
        student_name = st.text_input("Enter Your Name")
        roll_number = st.text_input("Enter Your Roll Number")
        questions = get_questions(quiz_id)
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
            end_time = datetime.now()
            record_submission(quiz_id, student_name, roll_number, start_time.strftime('%Y-%m-%d %H:%M:%S'),
                              end_time.strftime('%Y-%m-%d %H:%M:%S'), score, answers)
            st.success(f"Quiz submitted! Your score: {score}")
            cert_file = generate_certificate(student_name, quiz[1], score)
            st.download_button("Download Certificate", cert_file)
            del st.session_state['current_quiz']
            del st.session_state['quiz_start']
