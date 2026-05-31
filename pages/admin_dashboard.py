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

st.title("📊 Admin Dashboard")

df = pd.read_sql(
    "SELECT * FROM history",
    conn
)

col1,col2,col3 = st.columns(3)

col1.metric(
    "Total Predictions",
    len(df)
)

high = len(
    df[
        df["prediction"]
        .str.contains("High",na=False)
    ]
)

medium = len(
    df[
        df["prediction"]
        .str.contains("Medium",na=False)
    ]
)

low = len(
    df[
        df["prediction"]
        .str.contains("Low",na=False)
    ]
)

col2.metric(
    "High Risk",
    high
)

col3.metric(
    "Medium Risk",
    medium
)

st.metric(
    "Low Risk",
    low
)

st.subheader(
    "Risk Distribution"
)

st.bar_chart(
    df["prediction"].value_counts()
)