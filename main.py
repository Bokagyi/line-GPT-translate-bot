import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from openai import OpenAI

# Environment variables
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# Translation function using OpenAI
def translate_text(text, target_language_code):
    prompt = f"Translate this to {target_language_code}:\n\n{text}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Translation Error: {e}")
        return "Translation Error."

# LINE webhook endpoint
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# Handle text messages
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()

    if user_msg.startswith('@th '):
        original_text = user_msg[4:]
        translated = translate_text(original_text, target_language_code='Thai')
        reply = f"**Thai:** {translated}"
    elif user_msg.startswith('@my '):
        original_text = user_msg[4:]
        translated = translate_text(original_text, target_language_code='Burmese')
        reply = f"**Myanmar:** {translated}"
    elif user_msg.startswith('@en '):
        original_text = user_msg[4:]
        translated = translate_text(original_text, target_language_code='English')
        reply = f"**English:** {translated}"
    else:
        return  # Ignore unknown prefixes

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

# Run the Flask app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
