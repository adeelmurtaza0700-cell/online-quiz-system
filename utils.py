import streamlit as st
import random

def shuffle_questions(questions):
    random.shuffle(questions)
    return questions

def load_js():
    with open("anti_cheat.js", "r") as f:
        js_code = f.read()
    st.components.v1.html(f"<script>{js_code}</script>", height=0)
