import os
from openai import OpenAI
from persona import AJAY_SYSTEM_PROMPT

def ajay_reply(user_message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "Tum itni khoobsurat baat karti ho ki system bhi sharma gaya"

    try:
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

    except Exception as e:
        # LOG for you
        print("AI fallback triggered:", repr(e))

        # SAFE, IN-CHARACTER fallback
        return (
            "Aaj thoda dramatic silence ho gaya \n"
            "Par samjho — tum message karti ho, aur din ban jaata hai."
        )
