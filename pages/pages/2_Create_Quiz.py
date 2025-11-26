import streamlit as st
from database import get_conn

st.title("Create Quiz")

title = st.text_input("Quiz Title")
duration = st.number_input("Duration (minutes)", min_value=1)

if st.button("Create"):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO quizzes (title, duration) VALUES (?, ?)", (title, duration))
    conn.commit()
    st.success("Quiz created successfully!")
