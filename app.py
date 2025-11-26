import streamlit as st
from auth import register_user, login_user
from quiz import create_quiz, add_question
from evaluation import grade_quiz

st.title("Online Quiz and Exam System")

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
                # Add quiz creation UI here
            elif user.role == "student":
                st.subheader("Student Dashboard")
                # Add quiz taking UI here
        else:
            st.error("Invalid credentials")
