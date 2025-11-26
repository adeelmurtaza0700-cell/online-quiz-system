import streamlit as st
import time, json, os
from auth import register_user, login_user
from quiz import create_quiz, add_question, get_quizzes, get_questions, grade_quiz, get_results
from utils import generate_certificate

# Load JS for security
st.components.v1.html("""<script src="static/custom.js"></script>""", height=0)

st.title("Online Quiz & Exam System")

menu = ["Home", "Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "teacher"])
    if st.button("Register"):
        register_user(name, email, password, role)
        st.success("Account created successfully")

elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.success(f"Welcome {user.name} ({user.role})")

            if user.role == "teacher":
                st.subheader("Teacher Dashboard")
                teacher_menu = ["Create Quiz", "View Results"]
                t_choice = st.selectbox("Options", teacher_menu)

                if t_choice == "Create Quiz":
                    title = st.text_input("Quiz Title")
                    subject = st.text_input("Subject")
                    duration = st.number_input("Duration (minutes)", 1, 180)
                    instructions = st.text_area("Instructions")
                    if st.button("Create Quiz"):
                        quiz_id = create_quiz(title, subject, duration, instructions, user.id)
                        st.success(f"Quiz Created with ID: {quiz_id}")

                    st.subheader("Add Question")
                    quiz_list = get_quizzes()
                    q_quiz = st.selectbox("Select Quiz", [q.title for q in quiz_list])
                    question_text = st.text_area("Question Text")
                    q_type = st.selectbox("Question Type", ["MCQ", "True/False", "ShortAnswer"])
                    options = st.text_area("Options (comma-separated for MCQ)").split(",") if q_type=="MCQ" else None
                    correct_answer = st.text_input("Correct Answer")
                    if st.button("Add Question"):
                        selected_quiz_id = quiz_list[[q.title for q in quiz_list].index(q_quiz)].id
                        add_question(selected_quiz_id, question_text, q_type, options, correct_answer)
                        st.success("Question added successfully")

                elif t_choice == "View Results":
                    quizzes = get_quizzes()
                    selected_quiz = st.selectbox("Select Quiz", [q.title for q in quizzes])
                    if st.button("Show Results"):
                        quiz_id = quizzes[[q.title for q in quizzes].index(selected_quiz)].id
                        results = get_results(quiz_id)
                        for r in results:
                            st.write(f"Student ID: {r.user_id} | Score: {r.score} | Submitted: {r.submitted_at}")

            elif user.role == "student":
                st.subheader("Student Dashboard")
                quizzes = get_quizzes()
                selected_quiz = st.selectbox("Select Quiz to Take", [q.title for q in quizzes])
                if st.button("Start Quiz"):
                    quiz_id = quizzes[[q.title for q in quizzes].index(selected_quiz)].id
                    questions = get_questions(quiz_id)
                    answers = {}
                    for q in questions:
                        st.write(q.question_text)
                        if q.question_type=="MCQ":
                            opts = json.loads(q.options)
                            ans = st.radio("Choose answer", opts, key=str(q.id))
                        elif q.question_type=="True/False":
                            ans = st.radio("Choose answer", ["True","False"], key=str(q.id))
                        else:
                            ans = st.text_input("Your Answer", key=str(q.id))
                        answers[str(q.id)] = ans
                    if st.button("Submit Quiz"):
                        score = grade_quiz(user.id, quiz_id, answers)
                        st.success(f"Your Score: {score}/{len(questions)}")
                        file_path = f"{user.name}_{selected_quiz}.pdf"
                        generate_certificate(user.name, selected_quiz, score, file_path)
                        st.download_button("Download Certificate", file_path, file_name=file_path)
        else:
            st.error("Invalid credentials")
