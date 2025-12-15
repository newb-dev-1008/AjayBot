import os
from openai import OpenAI
from persona import AJAY_SYSTEM_PROMPT

def ajay_reply(user_message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("⚠️ OPENAI_API_KEY missing")
        return "Tum itni khoobsurat baat karti ho ki system bhi thoda shy ho gaya 😌"

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": AJAY_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.9,
        max_output_tokens=120
    )

    return response.output_text.strip()
