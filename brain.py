import os
from openai import OpenAI
from persona import AJAY_SYSTEM_PROMPT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_reply(user_message: str) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY missing")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": AJAY_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_output_tokens=120,
        temperature=0.9
    )

    return response.output_text.strip()
