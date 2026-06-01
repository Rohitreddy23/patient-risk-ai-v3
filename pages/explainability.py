import streamlit as st
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt

from utils.navigation import show_menu

# ==========================
# MENU
# ==========================

show_menu()

# ==========================
# AUTH
# ==========================

if "logged_in" not in st.session_state:
    st.error("Please login first")
    st.stop()

if st.session_state.role != "admin":
    st.error("Admin Access Only")
    st.stop()

# ==========================
# LOAD MODEL
# ==========================

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv("realtime_patient_data.csv")

features = [
    "Age",
    "Systolic_BP",
    "Diastolic_BP",
    "Cholesterol_Lvl",
    "Glucose_Lvl"
]

X = df[features]

# ==========================
# TITLE
# ==========================

st.title("📊 SHAP Explainability")

# ==========================
# FEATURE IMPORTANCE
# ==========================

st.subheader("Feature Importance")

importance = model.feature_importances_

imp_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

imp_df = imp_df.sort_values(
    by="Importance",
    ascending=False
)

st.dataframe(
    imp_df,
    use_container_width=True
)

fig1, ax1 = plt.subplots(figsize=(8, 4))

ax1.barh(
    imp_df["Feature"],
    imp_df["Importance"]
)

ax1.set_title(
    "Random Forest Feature Importance"
)

st.pyplot(fig1)

# ==========================
# SHAP SUMMARY
# ==========================

st.subheader("SHAP Summary Plot")

try:

    sample_data = X.sample(
        min(200, len(X)),
        random_state=42
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(
        sample_data
    )

    plt.figure(figsize=(10, 6))

    if isinstance(shap_values, list):

        shap.summary_plot(
            shap_values[0],
            sample_data,
            show=False
        )

    else:

        if len(shap_values.shape) == 3:

            shap.summary_plot(
                shap_values[:, :, 0],
                sample_data,
                show=False
            )

        else:

            shap.summary_plot(
                shap_values,
                sample_data,
                show=False
            )

    fig2 = plt.gcf()

    st.pyplot(fig2)

except Exception as e:

    st.error(
        f"SHAP Summary Plot Error: {e}"
    )

# ==========================
# SINGLE PATIENT ANALYSIS
# ==========================

st.subheader(
    "Single Patient Analysis"
)

patient_index = st.slider(
    "Select Patient Index",
    0,
    len(X) - 1,
    0
)

patient_data = X.iloc[
    patient_index:patient_index + 1
]

st.write(
    "Selected Patient Features"
)

st.dataframe(
    patient_data,
    use_container_width=True
)

prediction = model.predict(
    patient_data
)[0]

prediction_label = encoder.inverse_transform(
    [prediction]
)[0]

st.success(
    f"Prediction: {prediction_label}"
)

# ==========================
# PATIENT SHAP VALUES
# ==========================

try:

    single_shap = explainer.shap_values(
        patient_data
    )

    if isinstance(single_shap, list):

        values = single_shap[0][0]

    else:

        if len(single_shap.shape) == 3:

            values = single_shap[0, :, 0]

        elif len(single_shap.shape) == 2:

            values = single_shap[0]

        else:

            values = single_shap

    shap_df = pd.DataFrame({
        "Feature": features,
        "SHAP Value": values
    })

    st.subheader(
        "Feature Contribution"
    )

    st.dataframe(
        shap_df,
        use_container_width=True
    )

    fig3, ax3 = plt.subplots(
        figsize=(8, 4)
    )

    ax3.barh(
        shap_df["Feature"],
        shap_df["SHAP Value"]
    )

    ax3.set_title(
        "SHAP Feature Contributions"
    )

    st.pyplot(fig3)

except Exception as e:

    st.warning(
        f"Patient SHAP Analysis Error: {e}"
    )

# ==========================
# MODEL INSIGHTS
# ==========================

st.subheader(
    "Model Insights"
)

st.info(
    """
    SHAP explains how each feature influences the model prediction.

    Positive SHAP values increase the likelihood of the predicted class.

    Negative SHAP values decrease the likelihood of the predicted class.

    This helps make machine learning decisions transparent, interpretable,
    and trustworthy in healthcare applications.
    """
)