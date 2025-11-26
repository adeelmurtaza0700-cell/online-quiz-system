import streamlit as st
import time,json
from database import fetch_all, execute_query
from utils import start_timer

def start_exam():
    st.subheader("Available Quizzes")
    quizzes = fetch_all("SELECT * FROM quizzes")
    for q in quizzes:
        if st.button(f"Start {q['title']}", key=q['id']):
            run_quiz(q['id'], q['duration'])

def run_quiz(quiz_id,duration):
    questions = fetch_all("SELECT * FROM questions WHERE quiz_id=%s",(quiz_id,))
    answers = {}
    start_timer(duration)
    for q in questions:
        st.write(q['question_text'])
        if q['question_type']=="MCQ":
            ans = st.radio("Choose Option", options=q['options'])
        elif q['question_type']=="TrueFalse":
            ans = st.radio("True/False", ["True","False"])
        else:
            ans = st.text_input("Answer")
        answers[q['id']] = ans
    if st.button("Submit Exam"):
        score = grade_exam(quiz_id,answers)
        execute_query(
            "INSERT INTO results (student_id,quiz_id,answers,score,status) VALUES (%s,%s,%s,%s,%s)",
            (st.session_state.user['id'],quiz_id,json.dumps(answers),score,"passed" if score>=50 else "failed")
        )
        st.success(f"Exam submitted! Score: {score}")

def grade_exam(quiz_id,answers):
    questions = fetch_all("SELECT * FROM questions WHERE quiz_id=%s",(quiz_id,))
    score=0
    total=len(questions)
    for q in questions:
        if str(q['correct_answer']).strip()==str(answers.get(q['id'])).strip():
            score+=1
    return round(score/total*100,2)
