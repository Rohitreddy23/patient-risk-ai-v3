import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_report(patient_data, risk_level):

    prompt = f"""
    You are a healthcare AI assistant.

    Patient Information:
    {patient_data}

    Predicted Risk Level:
    {risk_level}

    Generate:

    1. Patient Health Summary
    2. Possible Risk Factors
    3. Lifestyle Recommendations
    4. Preventive Measures
    5. Follow-up Actions

    Keep it professional and easy to understand.

    Do not diagnose diseases.
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek/deepseek-chat",
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

    return data["choices"][0]["message"]["content"]