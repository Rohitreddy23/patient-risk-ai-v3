import streamlit as st
import requests
import os

from dotenv import load_dotenv

from utils.navigation import show_menu
from utils.rag import retrieve_context

# ==========================
# MENU
# ==========================

show_menu()

# ==========================
# LOGIN CHECK
# ==========================

if not st.session_state.get("logged_in", False):
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

st.title("🤖 AI Medical Chatbot (RAG)")

st.caption(
    "Ask healthcare-related questions using Retrieval-Augmented Generation (RAG)"
)

question = st.text_area(
    "Ask a medical question"
)

# ==========================
# ASK AI
# ==========================

if st.button("Ask AI"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            # RAG retrieval only when needed
            with st.spinner(
                "Searching medical records..."
            ):

                context = retrieve_context(
                    question
                )

            prompt = f"""
You are an AI healthcare assistant.

Relevant Medical Context:
{context}

User Question:
{question}

Instructions:
- Use the provided context.
- Give a concise answer.
- Do not diagnose diseases.
- Suggest consulting a healthcare professional when necessary.
"""

            with st.spinner(
                "Generating AI response..."
            ):

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
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
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

            st.info(
                context
            )

            st.subheader(
                "AI Response"
            )

            st.write(
                answer
            )

        except Exception as e:

            st.error(
                f"Chatbot Error: {e}"
            )