import streamlit as st
import pandas as pd
from utils.db import conn
from utils.navigation import show_menu

show_menu()

if "logged_in" not in st.session_state:
    st.error("Please login first")
    st.stop()

st.title("📜 Prediction History")

if st.session_state.role == "admin":

    query = """
    SELECT *
    FROM history
    ORDER BY prediction_date DESC
    """

else:

    query = f"""
    SELECT *
    FROM history
    WHERE username='{st.session_state.username}'
    ORDER BY prediction_date DESC
    """

df = pd.read_sql(query, conn)

st.write(
    f"Total Records: {len(df)}"
)

st.dataframe(
    df,
    width="stretch"
)