# app.py

import streamlit as st
import sqlite3
from datetime import datetime
from fpdf import FPDF
import random
import string

# ==============================
# Database Setup
# ==============================
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()

# Quizzes table
c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                subject TEXT NOT NULL,
                duration INTEGER NOT NULL,
                instructions TEXT,
                link TEXT UNIQUE
            )''')

# Questions table
c.execute('''CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                question TEXT NOT NULL,
                qtype TEXT NOT NULL,
                options TEXT,
                answer TEXT
            )''')

# Submissions table
c.execute('''CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER,
                student_name TEXT NOT NULL,
                roll_number TEXT NOT NULL,
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
    try:
        link = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        instructions = instructions if instructions else ""
        c.execute(
            "INSERT INTO quizzes (title, subject, duration, instructions, link) VALUES (?, ?, ?, ?, ?)",
            (title.strip(), subject.strip(), duration, instructions, link)
        )
        conn.commit()
        return link
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return None

def add_question(quiz_id, question, qtype, options, answer):
    try:
        c.execute(
            "INSERT INTO questions (quiz_id, question, qtype, options, answer) VALUES (?, ?, ?, ?, ?)",
            (quiz_id, question.strip(), qtype.strip(), options.strip() if options else "", answer.strip() if answer else "")
        )
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")

def get_quiz_by_link(link):
    c.execute("SELECT * FROM quizzes WHERE link=?", (link.strip(),))
    return c.fetchone()

def get_questions(quiz_id):
    c.execute("SELECT * FROM questions WHERE quiz_id=?", (quiz_id,))
    return c.fetchall()

def record_submission(quiz_id, student_name, roll_number, start_time, end_time, score, answers):
    try:
        c.execute(
            "INSERT INTO submissions (quiz_id, student_name, roll_number, start_time, end_time, score, answers) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (quiz_id, student_name.strip(), roll_number.strip(), start_time, end_time, score, str(answers))
        )
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")

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

st.title("Online Quiz System")

# ------------------------------
# Teacher Section: Create Quiz
# ------------------------------
st.subheader("Teacher Section - Create Quiz")
title = st.text_input("Quiz Title", key="quiz_title")
subject = st.text_input("Subject", key="quiz_subject")
duration = st.number_input("Duration (minutes)", 1, 180, key="quiz_duration")
instructions = st.text_area("Instructions", key="quiz_instructions")

if st.button("Create Quiz"):
    if not title.strip() or not subject.strip():
        st.error("Please fill in Quiz Title and Subject!")
    elif duration <= 0:
        st.error("Duration must be greater than 0!")
    else:
        link = create_quiz(title, subject, duration, instructions)
        if link:
            st.success(f"Quiz created! Share this link with students: **{link}**")
        else:
            st.error("Failed to create quiz!")

# ------------------------------
# Teacher Section: Add Questions
# ------------------------------
c.execute("SELECT * FROM quizzes ORDER BY id DESC")
quizzes = c.fetchall()
if quizzes:
    quiz_options = {q[1]: q[0] for q in quizzes}
    selected_quiz_name = st.selectbox("Select Quiz to Add Questions", list(quiz_options.keys()))
    selected_quiz_id = quiz_options[selected_quiz_name]
    question_text = st.text_area("Question")
    qtype = st.selectbox("Question Type", ["MCQ", "True/False", "Short Answer", "Fill in the blanks"])
    options_text = st.text_area("Options (comma separated for MCQ)")
    answer_text = st.text_input("Answer")
    if st.button("Add Question"):
        if not question_text.strip() or not qtype.strip():
            st.error("Please enter a question and select type!")
        else:
            add_question(selected_quiz_id, question_text, qtype, options_text, answer_text)
            st.success("Question added successfully!")

st.markdown("---")
# ------------------------------
# Student Section: Take Quiz
# ------------------------------
st.subheader("Student Section - Take Quiz via Link")

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
                opts = ques[4].split(",") if ques[4] else []
                if opts:
                    ans = st.radio("Select an option", opts, key=f"{ques[0]}")
                    answers[ques[0]] = ans
                else:
                    answers[ques[0]] = st.text_input("Answer", key=f"{ques[0]}")
            elif ques[3] == "True/False":
                ans = st.radio("Select True/False", ["True", "False"], key=f"{ques[0]}")
                answers[ques[0]] = ans
            else:
                ans = st.text_input("Answer", key=f"{ques[0]}")
                answers[ques[0]] = ans

        if st.button("Submit Quiz"):
            if not student_name.strip() or not roll_number.strip():
                st.error("Please enter your Name and Roll Number!")
            else:
                score = 0
                for ques in questions:
                    if ques[3] in ["MCQ", "True/False"] and answers.get(ques[0]) == ques[5]:
                        score += 1
                start_time = datetime.now()
                record_submission(
                    quiz[0],
                    student_name,
                    roll_number,
                    start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    score,
                    answers
                )
                st.success(f"Quiz submitted! Your score: {score}")
                cert_file = generate_certificate(student_name, quiz[1], score)
                st.download_button("Download Certificate", cert_file)
    else:
        st.error("Invalid quiz link!")
