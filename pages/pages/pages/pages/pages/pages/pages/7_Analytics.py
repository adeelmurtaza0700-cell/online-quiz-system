import streamlit as st
import pandas as pd
from database import get_conn

st.title("Admin Analytics")

conn = get_conn()
df = pd.read_sql_query("""
SELECT quizzes.title AS quiz, users.email AS student, score, date
FROM results
JOIN quizzes ON quizzes.id = results.quiz_id
JOIN users ON users.id = results.user_id
""", conn)

st.dataframe(df)

st.bar_chart(df[['score']])
