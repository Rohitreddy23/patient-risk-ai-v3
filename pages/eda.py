import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from utils.navigation import show_menu

show_menu()

if st.session_state.role != "admin":
    st.error("Admin Access Only")
    st.stop()
    
if "logged_in" not in st.session_state:
    st.error("Please login first")
    st.stop()
    
st.title("📊 EDA & Statistics")

df = pd.read_csv("realtime_patient_data.csv")

# =========================
# Dataset Preview
# =========================

st.subheader("Dataset Preview")
st.dataframe(df.head(), use_container_width=True)

# =========================
# Shape
# =========================

st.subheader("Dataset Shape")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

# =========================
# Data Types
# =========================

st.subheader("Data Types")

dtype_df = pd.DataFrame({
    "Column": df.columns,
    "Datatype": df.dtypes.astype(str)
})

st.dataframe(dtype_df)

# =========================
# Missing Values
# =========================

st.subheader("Missing Values")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum()
})

st.dataframe(missing_df)

# =========================
# Statistics
# =========================

st.subheader("Summary Statistics")

st.dataframe(df.describe())

# =========================
# Metrics
# =========================

st.subheader("Average Values")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Age",
        round(df["Age"].mean(), 2)
    )

with col2:
    st.metric(
        "Average Cholesterol",
        round(df["Cholesterol_Lvl"].mean(), 2)
    )

with col3:
    st.metric(
        "Average Glucose",
        round(df["Glucose_Lvl"].mean(), 2)
    )

# =========================
# Visualization
# =========================

st.subheader("Age Distribution")

fig, ax = plt.subplots()

ax.hist(
    df["Age"],
    bins=20
)

st.pyplot(fig)

# =========================
# Risk Score Distribution
# =========================

st.subheader("Risk Score Distribution")

fig2, ax2 = plt.subplots()

ax2.hist(
    df["Risk_Score"],
    bins=20
)

st.pyplot(fig2)

# =========================
# Test Results Count
# =========================

st.subheader("Test Results")

st.bar_chart(
    df["Test_Results"].value_counts()
)