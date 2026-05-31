import streamlit as st

for key in list(st.session_state.keys()):
    del st.session_state[key]

st.switch_page("app.py")