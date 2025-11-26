import streamlit as st
from database import init_db
from auth import send_otp, verify_otp

st.set_page_config(page_title="Online Exam System", layout="wide")
init_db()

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

st.title("Online Quiz & Exam Management System")


# ------------------- LOGIN PAGE -------------------
if not st.session_state.user:

    st.subheader("Login with Email + OTP")

    email = st.text_input("Enter Email Address")

    # Send OTP button
    if st.button("Send OTP"):
        if email.strip() == "":
            st.warning("Please enter an email first.")
        else:
            otp = send_otp(email)
            if otp:
                st.success(f"OTP sent! (Demo Mode → OTP: **{otp}**)")
                st.session_state.generated_otp = otp
                st.session_state.email_for_otp = email
            else:
                st.error("Failed to send OTP. Try again.")

    otp_in = st.text_input("Enter OTP", max_chars=6)

    # Verify OTP button
    if st.button("Verify OTP"):
        # Safety checks
        if "email_for_otp" not in st.session_state:
            st.error("Send OTP first.")
        elif otp_in.strip() == "":
            st.error("Enter the OTP.")
        else:
            user = verify_otp(st.session_state.email_for_otp, otp_in)

            if user:
                st.session_state.user = {
                    "id": user[0],
                    "email": st.session_state.email_for_otp,
                    "role": user[1]
                }
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid OTP. Please try again.")

else:
    # ------------- LOGGED-IN DASHBOARD -------------
    if st.session_state.user:
        st.success(f"Logged in as: {st.session_state.user['email']}")
        st.sidebar.success(f"Logged in: {st.session_state.user['email']}")
        st.sidebar.info("Use the sidebar to navigate pages.")

    else:
        st.warning("User session not found. Please log in.")
