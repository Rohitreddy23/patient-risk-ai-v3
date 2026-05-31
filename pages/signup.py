import streamlit as st
from utils.db import conn, cursor


st.title("📝 Signup")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

role = st.selectbox(
    "Role",
    ["patient", "admin"]
)

if st.button("Create Account"):

    try:

        cursor.execute(
            """
            INSERT INTO users(
            username,
            password,
            role
            )
            VALUES(?,?,?)
            """,
            (
                username,
                password,
                role
            )
        )

        conn.commit()

        st.success("Account Created")

    except:

        st.error("Username Already Exists")