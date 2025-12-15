import os
from openai import OpenAI
from persona import AJAY_SYSTEM_PROMPT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ajay_reply(user_message: str, chat_history: list | None = None) -> str:
    """
    Generates Ajay-style reply to the user's message.
    """

    messages = [
        {"role": "system", "content": AJAY_SYSTEM_PROMPT}
    ]

    if chat_history:
        for msg in chat_history[-6:]:
            messages.append(msg)

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # fast + cheap + good personality
        messages=messages,
        temperature=0.9,
        max_tokens=120
    )

    return response.choices[0].message.content.strip()
