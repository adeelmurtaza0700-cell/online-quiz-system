import streamlit as st
from database import execute_query, fetch_all

def create_quiz():
    st.subheader("Create New Quiz")
    title = st.text_input("Quiz Title")
    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", min_value=5,max_value=180)
    instructions = st.text_area("Instructions")
    start_time = st.text_input("Start Time (YYYY-MM-DD HH:MM)")
    end_time = st.text_input("End Time (YYYY-MM-DD HH:MM)")
    if st.button("Create Quiz"):
        execute_query(
            "INSERT INTO quizzes (title,subject,duration,instructions,start_time,end_time,created_by) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (title,subject,duration,instructions,start_time,end_time,st.session_state.user['id'])
        )
        st.success("Quiz Created!")

def view_quizzes():
    st.subheader("All Quizzes")
    quizzes = fetch_all("SELECT * FROM quizzes")
    for q in quizzes:
        st.write(f"**ID {q['id']}** - {q['title']} | {q['subject']} | {q['duration']} min")
