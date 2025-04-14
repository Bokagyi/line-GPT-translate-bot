from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from googletrans import Translator

app = Flask(__name__)

# LINE Channel access token & secret
line_bot_api = LineBotApi('Pv1eu8jUfgJTIcC1eMApXIGbaXYIMIAAt/JqpKW7FlX5LrRdCu/X+wqxauNokT0zUcxe4oQOavmO7hPyImk70qR1bm+P3s/zHJrTWx3hClqVjP9YPz2SysPFwClAYLB8lHJ4CO9wWO2VqGxHs8LUGgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6be49243075ab0f2df93eb9a442c2601')

# Google Translator instance
translator = Translator()

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
    input_text = event.message.text

    # Translate Burmese to English
    try:
        translated = translator.translate(input_text, src='my', dest='en').text
    except Exception as e:
        translated = "ဘာသာပြန်ရာမှာ အမှားရှိနေပါတယ်။"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=translated)
    )

if __name__ == "__main__":
    app.run()
