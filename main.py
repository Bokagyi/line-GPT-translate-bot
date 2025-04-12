from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Set your keys
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

class Event(BaseModel):
    type: str
    replyToken: str = None
    message: dict = None

class WebhookBody(BaseModel):
    events: list[Event]

async def translate_text(text: str) -> str:
    prompt = f"Translate this between Burmese and Thai automatically:\n\n{text}\n\nTranslation:"
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

async def reply_to_line(reply_token: str, message: str):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    async with httpx.AsyncClient() as client:
        await client.post("https://api.line.me/v2/bot/message/reply", json=body, headers=headers)

@app.post("/webhook")
async def webhook(req: Request):
    body = await req.json()
    if "events" not in body:
        return {"status": "ok"}

    for event in body["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_text = event["message"]["text"]
            reply_token = event["replyToken"]
            translated = await translate_text(user_text)
            await reply_to_line(reply_token, translated)
    return {"status": "ok"}
    
