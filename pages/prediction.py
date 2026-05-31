import streamlit as st
import pandas as pd
import pickle

from utils.db import conn, cursor
from utils.ai_helper import generate_report
from utils.navigation import show_menu

show_menu()

# =========================
# LOGIN CHECK
# =========================

if "logged_in" not in st.session_state:
    st.error("Please login first")
    st.stop()

# =========================
# LOAD MODEL
# =========================

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# =========================
# PAGE TITLE
# =========================

st.title("🏥 Patient Risk Prediction")

st.write(
    f"Welcome **{st.session_state.username}**"
)

# =========================
# INPUTS
# =========================

age = st.number_input(
    "Age",
    1,
    120,
    40
)

systolic = st.number_input(
    "Systolic BP",
    50,
    250,
    120
)

diastolic = st.number_input(
    "Diastolic BP",
    30,
    200,
    80
)

cholesterol = st.number_input(
    "Cholesterol Level",
    50,
    500,
    180
)

glucose = st.number_input(
    "Glucose Level",
    50,
    500,
    100
)

# =========================
# PREDICT
# =========================

if st.button("Predict Risk"):

    input_df = pd.DataFrame(
        [[
            age,
            systolic,
            diastolic,
            cholesterol,
            glucose
        ]],
        columns=[
            "Age",
            "Systolic_BP",
            "Diastolic_BP",
            "Cholesterol_Lvl",
            "Glucose_Lvl"
        ]
    )

    prediction = model.predict(input_df)[0]

    result = encoder.inverse_transform(
        [prediction]
    )[0]

    probabilities = model.predict_proba(
        input_df
    )

    confidence = round(
        max(probabilities[0]) * 100,
        2
    )

    # =========================
    # RISK MAPPING
    # =========================

    risk_mapping = {
        "Normal": "🟢 Low Risk",
        "Inconclusive": "🟡 Medium Risk",
        "Abnormal": "🔴 High Risk"
    }

    risk_level = risk_mapping.get(
        result,
        result
    )

    st.success(
        f"Risk Level: {risk_level}"
    )

    st.metric(
        "Prediction Confidence",
        f"{confidence}%"
    )

    st.subheader(
        "Patient Inputs"
    )

    st.dataframe(input_df)

    # =========================
    # SAVE HISTORY
    # =========================

    cursor.execute(
        """
        INSERT INTO history(
            username,
            age,
            systolic,
            diastolic,
            cholesterol,
            glucose,
            prediction
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            st.session_state.username,
            age,
            systolic,
            diastolic,
            cholesterol,
            glucose,
            risk_level
        )
    )

    conn.commit()

    st.success(
        "Prediction saved successfully."
    )

    # =========================
    # AI REPORT
    # =========================

    with st.spinner(
        "Generating AI Health Assessment..."
    ):

        patient_data = {
            "Age": age,
            "Systolic_BP": systolic,
            "Diastolic_BP": diastolic,
            "Cholesterol_Lvl": cholesterol,
            "Glucose_Lvl": glucose
        }

        report = generate_report(
            patient_data,
            risk_level
        )

    st.subheader(
        "🤖 AI Health Assessment"
    )

    st.write(report)