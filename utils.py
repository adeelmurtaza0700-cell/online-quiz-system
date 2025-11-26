import streamlit as st

def tab_alert():
    st.markdown("""
    <script>
    document.addEventListener('visibilitychange', function() {
        if(document.hidden) {
            alert('You switched tabs! This will be logged.');
        }
    });
    </script>
    """, unsafe_allow_html=True)
