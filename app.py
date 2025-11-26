import streamlit as st
from auth import login_user, register_user

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create Account")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["student", "teacher", "admin"])

        if st.button("Register"):
            # Validate input
            if not name or not email or not password:
                st.error("All fields are required!")
            else:
                success, msg = register_user(name, email, password, role)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    elif choice == "Login":
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user, msg = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success(f"{msg} Welcome {user['name']}!")
            else:
                st.error(msg)
