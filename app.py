import streamlit as st
from database import init_db
from auth import send_otp, verify_otp

st.set_page_config(page_title="Online Exam System", layout="wide")
init_db()

# Session
if "user" not in st.session_state:
    st.session_state.user = None

st.title("Online Quiz & Exam Management System")

# -------------- LOGIN SCREEN --------------
if not st.session_state.user:

    email = st.text_input("Enter Email Address")

    # Send OTP
    if st.button("Send OTP"):
        otp = send_otp(email)
        st.success(f"OTP sent! (Demo Mode → OTP: **{otp}**)")

    otp_in = st.text_input("Enter OTP")

    # Verify
    if st.button("Verify OTP"):
        user = verify_otp(email, otp_in)
        if user:
            st.session_state.user = {
                "id": user[0],
                "email": email,
                "role": user[1]
            }
            st.rerun()
        else:
            st.error("Invalid OTP. Try again.")

else:
    st.success(f"Logged in as: {st.session_state.user['email']}")
    st.sidebar.info("Use the pages sidebar to navigate.")
