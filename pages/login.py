import streamlit as st
from utils.db import conn, cursor

# If already logged in, redirect
if st.session_state.get("logged_in", False):

    if st.session_state.role == "admin":
        st.switch_page("pages/admin_dashboard.py")
    else:
        st.switch_page("pages/home.py")

st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    cursor.execute(
        """
        SELECT role
        FROM users
        WHERE username=?
        AND password=?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    if user:

        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = user[0]

        st.switch_page("app.py")
        
    else:

        st.error("Invalid Credentials")