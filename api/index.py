from flask import Flask, request, json, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.llm import ChatGPT
import requests
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


# 啟動LINE的loading動畫
def start_loading_animation(chat_id, loading_seconds):
    url = "https://api.line.me/v2/bot/chat/loading/start"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {line_bot_api.channel_access_token}',
    }
    data = {
        "chatId": chat_id,
        "loadingSeconds": loading_seconds
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

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
    """
    This function handles LINE MessageAPI messages. 
    It checks if the message is a text message and processes it accordingly.
    If the message starts with "啟動", it sets the working_status to True.
    If the message starts with "關閉", it sets the working_status to False.
    If the working_status is True, it sends the message to ChatGPT to get a response and sends the response back to the user.
    """


if __name__ == "__main__":
    app.run()
