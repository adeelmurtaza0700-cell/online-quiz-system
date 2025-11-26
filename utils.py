import streamlit as st
import time

def start_timer(minutes):
    st.info(f"Exam Timer: {minutes} minutes")
    for i in range(minutes*60,0,-1):
        st.progress(i/(minutes*60))
        time.sleep(1)
