import streamlit as st

def show_menu():

    if st.session_state.role == "admin":

        st.sidebar.title("Admin Menu")

        if st.sidebar.button("Dashboard"):
            st.switch_page("pages/admin_dashboard.py")

        if st.sidebar.button("EDA"):
            st.switch_page("pages/eda.py")

        if st.sidebar.button("Explainability"):
            st.switch_page("pages/explainability.py")

        if st.sidebar.button("Users"):
            st.switch_page("pages/user_management.py")

        if st.sidebar.button("History"):
            st.switch_page("pages/history.py")

        if st.sidebar.button("Chatbot"):
            st.switch_page("pages/chatbot.py")

        if st.sidebar.button("Logout"):
            st.switch_page("pages/logout.py")

    else:

        st.sidebar.title("Patient Menu")

        if st.sidebar.button("Home"):
            st.switch_page("pages/home.py")

        if st.sidebar.button("Prediction"):
            st.switch_page("pages/prediction.py")

        if st.sidebar.button("History"):
            st.switch_page("pages/history.py")

        if st.sidebar.button("Reports"):
            st.switch_page("pages/reports.py")

        if st.sidebar.button("Chatbot"):
            st.switch_page("pages/chatbot.py")

        if st.sidebar.button("Logout"):
            st.switch_page("pages/logout.py")