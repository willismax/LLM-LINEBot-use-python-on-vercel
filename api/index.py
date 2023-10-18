from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.llm import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
web_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return '<h1>Hello Word</h1>'


# Listen for all Post Requests from /callback
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        web_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@web_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """LINE MessageAPI message processing"""
    if event.source.user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'
    
    global working_status
    if event.message.type != "text":
        return

    if event.message.text[:3] == "啟動":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="啟動"))
        return

    if event.message.text[:3] == "關閉":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ChatGPT休眠去"))
        return

    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"助教:{reply_msg}"))


if __name__ == "__main__":
    app.run()