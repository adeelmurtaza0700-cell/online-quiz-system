import streamlit as st
from database import init_db
from auth import send_otp, verify_otp

st.set_page_config(page_title="Online Exam System", layout="wide")
init_db()

if "user" not in st.session_state:
    st.session_state.user = None

st.title("Online Quiz & Exam Management System")

if not st.session_state.user:
    email = st.text_input("Enter Email to Login")
    if st.button("Send OTP"):
        otp = send_otp(email)
        st.success(f"Your OTP is: {otp}")  # Remove in production

    verify_code = st.text_input("Enter OTP")
    if st.button("Verify"):
        user = verify_otp(email, verify_code)
        if user:
            st.session_state.user = user
            st.experimental_rerun()
        else:
            st.error("Invalid OTP")
else:
    st.success(f"Logged in as {st.session_state.user[1]}")
    st.sidebar.success("Use the sidebar menu to navigate pages.")
