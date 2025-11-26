import streamlit as st
from database import fetch_all

def view_results(student_id):
    st.subheader("Your Results")
    results = fetch_all("SELECT quizzes.title, results.score, results.status FROM results JOIN quizzes ON quizzes.id=results.quiz_id WHERE student_id=%s",(student_id,))
    for r in results:
        st.write(f"{r['title']} | Score: {r['score']} | Status: {r['status']}")

def leaderboard(quiz_id):
    results = fetch_all("SELECT users.name, results.score FROM results JOIN users ON users.id=results.student_id WHERE quiz_id=%s ORDER BY score DESC",(quiz_id,))
    return results
