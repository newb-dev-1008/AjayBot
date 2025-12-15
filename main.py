from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import os
from dotenv import load_dotenv
from db import save_message
from brain import ajay_reply

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

WHATSAPP_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

# @app.get("/webhook")
# def verify(hub_mode: str, hub_challenge: str, hub_verify_token: str):
#     if hub_verify_token == VERIFY_TOKEN:
#         return int(hub_challenge)
#     return "Verification failed"

# @app.get("/webhook")
# async def verify_webhook(request: Request):
#     params = request.query_params
# 
#     mode = params.get("hub.mode")
#     token = params.get("hub.verify_token")
#     challenge = params.get("hub.challenge")
# 
#     if mode == "subscribe" and token == VERIFY_TOKEN:
#         return PlainTextResponse(challenge, status_code=200)
# 
#     return PlainTextResponse("Forbidden", status_code=403)

# @app.post("/webhook")
# async def webhook(request: Request):
#     data = await request.json()
# 
#     try:
#         entry = data["entry"][0]
#         change = entry["changes"][0]
#         value = change["value"]
# 
#         messages = value.get("messages")
#         if not messages:
#             return {"status": "ok"}
# 
#         message = messages[0]
#         from_number = message["from"]
#         text = message["text"]["body"]
# 
#         reply_text = generate_ajay_reply(text)
# 
#         send_message(from_number, reply_text)
# 
#     except Exception as e:
#         print("Webhook error:", e)
# 
#     return {"status": "ok"}

# def generate_ajay_reply(user_text: str) -> str:
#     return (
#         "Tumhe lagta hai main reply nahi karunga? 😏\n\n"
#         "Ajay hoon main. Bollywood villain energy ke saath.\n"
#         "Aur haan — tum khud ek gift ho."
#     )

def send_message(to, text):
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    r = requests.post(WHATSAPP_URL, json=payload, headers=headers)
    print("Sent:", r.status_code, r.text)

@app.post("/webhook")
async def handle_message(request: Request):
    data = await request.json()

    try:
        entry = data["entry"][0]
        change = entry["changes"][0]["value"]
        messages = change.get("messages")

        if messages:
            from_number = messages[0]["from"]
            user_text = messages[0]["text"]["body"]

            reply = ajay_reply(user_text)

            send_message(
                to=from_number,
                text=reply
            )

    except Exception as e:
        print("Webhook error:", e)

    return {"status": "ok"}
