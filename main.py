from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from googletrans import Translator

app = Flask(__name__)

# Replace with your own channel access token and secret
LINE_CHANNEL_ACCESS_TOKEN = 'Pv1eu8jUfgJTIcC1eMApXIGbaXYIMIAAt/JqpKW7FlX5LrRdCu/X+wqxauNokT0zUcxe4oQOavmO7hPyImk70qR1bm+P3s/zHJrTWx3hClqVjP9YPz2SysPFwClAYLB8lHJ4CO9wWO2VqGxHs8LUGgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '6be49243075ab0f2df93eb9a442c2601'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    user_text = event.message.text

    translator = Translator()
    try:
        translation = translator.translate(user_text, src='my', dest='en')
        reply_text = f"ဘာသာပြန်ချက်: {translation.text}"
    except Exception as e:
        reply_text = f"ဘာသာပြန်မရပါ: {str(e)}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
