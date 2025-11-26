import streamlit as st
from database import get_conn

st.title("Leaderboard")

conn = get_conn()
c = conn.cursor()

rows = c.execute("""
SELECT users.email, quizzes.title, results.score 
FROM results
JOIN users ON users.id = results.user_id
JOIN quizzes ON quizzes.id = results.quiz_id
ORDER BY score DESC
""").fetchall()

st.table(rows)
