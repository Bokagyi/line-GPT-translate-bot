import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")
line_bot_api = LineBotApi(os.getenv("Pv1eu8jUfgJTIcC1eMApXIGbaXYIMIAAt/JqpKW7FlX5LrRdCu/X+wqxauNokT0zUcxe4oQOavmO7hPyImk70qR1bm+P3s/zHJrTWx3hClqVjP9YPz2SysPFwClAYLB8lHJ4CO9wWO2VqGxHs8LUGgdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.getenv("6be49243075ab0f2df93eb9a442c2601"))

def translate_with_gpt(text):
    prompt = f"Translate the following text between Burmese and Thai automatically:\n\n{text}\n\nTranslation:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translation assistant that translates between Burmese and Thai."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text
    translated = translate_with_gpt(user_input)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translated)
    )

if __name__ == "__main__":
    app.run()
