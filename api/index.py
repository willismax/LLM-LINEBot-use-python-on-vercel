import os
from api.llm import ChatGPT
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage

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
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
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
        

@web_handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # 處理圖片訊息
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(f"{event.message.id}.jpg", "wb") as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    # 調用OpenAI API進行圖片處理
    with open(f"{event.message.id}.jpg", "rb") as image_file:
        reply_msg = chatgpt.Image.create(
            file=image_file,
            purpose='text_detection'
        )
    
    # 假設OpenAI回傳的結果包含在response['data']['text']
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
