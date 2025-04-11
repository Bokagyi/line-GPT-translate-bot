from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

# LINE Channel Secret & Access Token
LINE_CHANNEL_ACCESS_TOKEN = 'Pv1eu8jUfgJTIcC1eMApXIGbaXYIMIAAt/JqpKW7FlX5LrRdCu/X+wqxauNokT0zUcxe4oQOavmO7hPyImk70qR1bm+P3s/zHJrTWx3hClqVjP9YPz2SysPFwClAYLB8lHJ4CO9wWO2VqGxHs8LUGgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '6be49243075ab0f2df93eb9a442c2601'
OPENAI_API_KEY = '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'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    # Translate via OpenAI
    translation = translate_text(user_input)

    # Reply to LINE user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translation)
    )

def translate_text(text):
    prompt = f"""Translate the following text into Burmese, Thai, and English:\n\nText: {text}\n\nTranslations:\n- Burmese:\n- Thai:\n- English:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    app.run()
