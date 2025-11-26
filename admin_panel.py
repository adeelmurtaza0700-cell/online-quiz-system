import streamlit as st
from database import add_quiz, get_quizzes, add_question, get_questions, get_leaderboard

def admin_dashboard():
    st.title("Admin Dashboard")
    menu = ["Create Quiz", "Add Questions", "Analytics", "Leaderboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Quiz":
        title = st.text_input("Quiz Title")
        if st.button("Create"):
            add_quiz(title)
            st.success("Quiz created!")
    
    elif choice == "Add Questions":
        quizzes = get_quizzes().data
        quiz = st.selectbox("Select Quiz", quizzes, format_func=lambda x: x['title'])
        question = st.text_area("Question")
        opt1 = st.text_input("Option 1")
        opt2 = st.text_input("Option 2")
        opt3 = st.text_input("Option 3")
        opt4 = st.text_input("Option 4")
        answer = st.selectbox("Correct Answer", [opt1, opt2, opt3, opt4])
        if st.button("Add Question"):
            add_question(quiz['id'], question, opt1, opt2, opt3, opt4, answer)
            st.success("Question added!")

    elif choice == "Analytics":
        quizzes = get_quizzes().data
        for q in quizzes:
            questions = get_questions(q['id']).data
            st.write(f"Quiz: {q['title']}, Total Questions: {len(questions)}")

    elif choice == "Leaderboard":
        leaderboard = get_leaderboard().data
        st.table(leaderboard)
