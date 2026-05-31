import streamlit as st
import pandas as pd

from utils.db import conn
from utils.navigation import show_menu

show_menu()

if "logged_in" not in st.session_state:
    st.stop()

st.title("📄 Reports")

query = f"""
SELECT *
FROM history
WHERE username='{st.session_state.username}'
"""

df = pd.read_sql(
    query,
    conn
)

st.dataframe(df)

csv = df.to_csv(index=False)

st.download_button(
    "Download CSV Report",
    csv,
    "patient_report.csv",
    "text/csv"
)