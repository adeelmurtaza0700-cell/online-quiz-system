import streamlit as st
from database import get_conn

st.title("Add Questions to Quiz")
conn = get_conn()
c = conn.cursor()

quizzes = c.execute("SELECT id, title FROM quizzes").fetchall()
quiz = st.selectbox("Choose Quiz", quizzes, format_func=lambda x: x[1])

q = st.text_area("Question")
o1 = st.text_input("Option 1")
o2 = st.text_input("Option 2")
o3 = st.text_input("Option 3")
o4 = st.text_input("Option 4")
ans = st.selectbox("Correct Answer", [o1, o2, o3, o4])

if st.button("Add"):
    c.execute("""INSERT INTO questions 
                (quiz_id, question, opt1, opt2, opt3, opt4, answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (quiz[0], q, o1, o2, o3, o4, ans))
    conn.commit()
    st.success("Question added!")
