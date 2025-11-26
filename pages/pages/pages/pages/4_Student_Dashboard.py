import streamlit as st
from database import get_conn

st.title("Student Dashboard")

conn = get_conn()
c = conn.cursor()

quizzes = c.execute("SELECT id, title FROM quizzes").fetchall()

quiz = st.selectbox("Available Quizzes", quizzes, format_func=lambda x: x[1])

if st.button("Start Exam"):
    st.session_state.selected_quiz = quiz
    st.switch_page("pages/5_Take_Exam.py")
