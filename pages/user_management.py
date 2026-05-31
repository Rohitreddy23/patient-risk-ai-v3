import streamlit as st
import pandas as pd

from utils.db import conn
from utils.navigation import show_menu

show_menu()

if "logged_in" not in st.session_state:
    st.stop()

if st.session_state.role != "admin":
    st.error("Admin Access Only")
    st.stop()

st.title("👥 User Management")

users = pd.read_sql(
    """
    SELECT
        id,
        username,
        role
    FROM users
    """,
    conn
)

st.dataframe(
    users,
    width="stretch"
)

st.metric(
    "Total Users",
    len(users)
)