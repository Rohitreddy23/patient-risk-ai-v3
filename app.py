import streamlit as st

st.set_page_config(
    page_title="Patient Risk Assessment",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🏥 Patient Risk Assessment System")

# NOT LOGGED IN
if not st.session_state.logged_in:

    st.subheader("Welcome")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.switch_page("pages/login.py")

    with col2:
        if st.button("Signup"):
            st.switch_page("pages/signup.py")

# ADMIN
elif st.session_state.role == "admin":

    st.sidebar.success(
        f"Admin: {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Admin Dashboard",
            "EDA",
            "Explainability",
            "User Management",
            "History",
            "Chatbot",
            "Logout"
        ]
    )

    if page == "Home":
        st.switch_page("pages/home.py")

    elif page == "Admin Dashboard":
        st.switch_page("pages/admin_dashboard.py")

    elif page == "EDA":
        st.switch_page("pages/eda.py")

    elif page == "Explainability":
        st.switch_page("pages/explainability.py")

    elif page == "User Management":
        st.switch_page("pages/user_management.py")

    elif page == "History":
        st.switch_page("pages/history.py")

    elif page == "Chatbot":
        st.switch_page("pages/chatbot.py")

    elif page == "Logout":
        st.switch_page("pages/logout.py")

# PATIENT
else:

    st.sidebar.success(
        f"Patient: {st.session_state.username}"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Prediction",
            "History",
            "Reports",
            "Chatbot",
            "Logout"
        ]
    )

    if page == "Home":
        st.switch_page("pages/home.py")

    elif page == "Prediction":
        st.switch_page("pages/prediction.py")

    elif page == "History":
        st.switch_page("pages/history.py")

    elif page == "Reports":
        st.switch_page("pages/reports.py")

    elif page == "Chatbot":
        st.switch_page("pages/chatbot.py")

    elif page == "Logout":
        st.switch_page("pages/logout.py")