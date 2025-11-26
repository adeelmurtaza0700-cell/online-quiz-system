import streamlit as st
from auth import signup, login
from admin import admin_dashboard
from student import student_dashboard
from database import supabase

st.set_page_config(page_title="Online Quiz System", layout="wide")

# --- Session State ---
if "user" not in st.session_state:
    st.session_state.user = None

st.title("📝 Online Quiz & Exam Management System")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

# --- Signup ---
if choice == "Signup":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin", "student"])
    if st.button("Create Account"):
        if signup(username, password, role):
            st.success("Account created! Login now.")
        else:
            st.error("Username already exists.")

# --- Login ---
elif choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.user = user
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password.")

# --- After login ---
if st.session_state.user:
    user = st.session_state.user
    st.sidebar.success(f"Logged in as {user['role']} | {user['username']}")

    if user["role"] == "admin":
        admin_dashboard()
    else:
        student_dashboard(user)
