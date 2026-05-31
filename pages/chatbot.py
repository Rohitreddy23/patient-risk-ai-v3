import streamlit as st
import requests
import os

from dotenv import load_dotenv
from utils.rag import retrieve_context
from utils.navigation import show_menu

# ==========================
# MENU
# ==========================

show_menu()

# ==========================
# LOGIN CHECK
# ==========================

if "logged_in" not in st.session_state:
    st.error("Please login first")
    st.stop()

# ==========================
# ENV
# ==========================

load_dotenv()

API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

# ==========================
# PAGE
# ==========================

st.title(
    "🤖 AI Medical Chatbot (RAG)"
)

question = st.text_area(
    "Ask a medical question"
)

# ==========================
# ASK
# ==========================

if st.button("Ask AI"):

    if question:

        with st.spinner(
            "Searching medical records..."
        ):

            context = retrieve_context(
                question
            )

        prompt = f"""
        You are a healthcare assistant.

        Relevant Medical Context:
        {context}

        User Question:
        {question}

        Instructions:
        - Use the context above.
        - Provide a clear answer.
        - Do not diagnose diseases.
        - Suggest consulting a healthcare professional when needed.
        """

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization":
                f"Bearer {API_KEY}",
                "Content-Type":
                "application/json"
            },
            json={
                "model":
                "deepseek/deepseek-chat",
                "messages":[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        answer = data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

        st.subheader(
            "Retrieved Context"
        )

        st.info(context)

        st.subheader(
            "AI Response"
        )

        st.write(answer)