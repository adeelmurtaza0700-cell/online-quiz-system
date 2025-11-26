import streamlit as st
from database import get_quizzes, get_questions, save_result
import random, time
from utils import tab_alert
from certificate import generate_certificate

def student_dashboard(user):
    st.title("Student Dashboard")

    quizzes = get_quizzes().data
    quiz = st.selectbox("Select Quiz", quizzes, format_func=lambda x: x['title'])

    if st.button("Start Quiz"):
        take_quiz(user, quiz['id'], quiz['title'])

def take_quiz(user, quiz_id, quiz_title):
    questions = get_questions(quiz_id).data
    random.shuffle(questions)  # Random questions

    st.warning("Exam started! Timer is 5 mins")
    start_time = time.time()
    duration = 5 * 60  # 5 minutes

    score = 0
    for q in questions:
        if time.time() - start_time > duration:
            st.error("Time is up!")
            break

        tab_alert()  # Detect tab switch
        st.write(f"### {q['question']}")
        ans = st.radio("Choose", [q['opt1'], q['opt2'], q['opt3'], q['opt4']], key=q['id'])
        if ans == q['answer']:
            score += 1

    if st.button("Submit"):
        save_result(user['id'], quiz_id, score)
        st.success(f"Your Score: {score}")
        generate_certificate(user['username'], quiz_title, score)
