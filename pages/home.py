import streamlit as st
import pandas as pd
from utils.db import conn
from utils.navigation import show_menu

show_menu()

if "logged_in" not in st.session_state:
    st.stop()

st.title("🏥 Patient Risk Assessment System")

history = pd.read_sql(
    "SELECT * FROM history",
    conn
)

st.success(
    f"Welcome {st.session_state.username}"
)

c1,c2,c3 = st.columns(3)

c1.metric(
    "Predictions",
    len(history)
)

c2.metric(
    "Users",
    len(
        pd.read_sql(
            "SELECT * FROM users",
            conn
        )
    )
)

c3.metric(
    "High Risk Cases",
    len(
        history[
            history["prediction"]
            .str.contains(
                "High",
                na=False
            )
        ]
    )
)