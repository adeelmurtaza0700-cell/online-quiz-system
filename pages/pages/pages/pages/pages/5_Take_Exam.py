import streamlit as st
from database import get_conn
from utils import shuffle_questions, load_js

st.title("Take Exam")

load_js()   # Anti-cheat

quiz = st.session_state.selected_quiz
conn = get_conn()
c = conn.cursor()

# Get quiz duration
dur = c.execute("SELECT duration FROM quizzes WHERE id=?", (quiz[0],)).fetchone()[0]

# Timer
if "time_left" not in st.session_state:
    st.session_state.time_left = dur * 60

st.info(f"Time Left: {st.session_state.time_left} seconds")

questions = c.execute("SELECT * FROM questions WHERE quiz_id=?", (quiz[0],)).fetchall()
questions = shuffle_questions(list(questions))

score = 0
answers = {}

for q in questions:
    ans = st.radio(q[2], [q[3], q[4], q[5], q[6]], key=q[0])
    answers[q[0]] = ans

if st.button("Submit Exam"):
    for q in questions:
        if answers[q[0]] == q[7]:
            score += 1

    c.execute("INSERT INTO results (user_id, quiz_id, score, date) VALUES (?, ?, ?, DATE('now'))",
              (st.session_state.user[0], quiz[0], score))
    conn.commit()

    st.success(f"Your Score: {score}")
