from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)
from llm import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()


# domain root
@app.route('/')
def home():
    return 'https://github.com/willismax/LLM-LINEBot-use-python-on-vercel'

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
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    """LINE MessageAPI message processing"""
    if event.source.user_id =='Udeadbeefdeadbeefdeadbeefdeadbeef':
        return 'OK'

    # 處裡圖片的方式: 上傳圖床、存HackMD暫存筆記
    if event.message.type=='image':
        image = line_bot_api.get_message_content(event.message.id)
        content = hb.flex_reply_image(image)
        message = FlexSendMessage(
            alt_text = "圖片已上傳至HackMD",
            contents = content
        )
        line_bot_api.reply_message(event.reply_token, message)

    if event.message.type=='text':
        word =  str(event.message.text)

        # 測試API回傳內容
        if word[:5] == "@test":
            message = TextSendMessage(text=str(event))
            line_bot_api.reply_message(event.reply_token, message)
        
        # OpenAI API回應
        elif word[:3] == "@ai":
            content = event.message.text
            chatgpt.add_msg(f"HUMAN:{content}?\n")
            reply_msg = chatgpt.get_response()
            hb.update_ai_note(content,reply_msg)  #將回應紀錄於HackMD
            message = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(event.reply_token, message)

        # Google翻譯    
        elif event.message.text[:3] == "@翻英":
            content = mf.translate_text(event.message.text[3:], "en")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text[:3] == "@翻日":
            content = mf.translate_text(event.message.text[3:] , "ja")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        elif event.message.text[:3] == "@翻中":
            content = mf.translate_text(event.message.text[3:] , "zh-tw")
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)

        # 呼叫選單
        elif event.message.text[:3] == "@選單":
            content = f"使用說明:\n- 功能: @test、@翻日、@翻中、@ai\n無關鍵字則存: https://hackmd.io/{TEMP_NOTE_ID}"
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)
        
        # 無關鍵字則增至HackMD暫存筆記
        else: 
            content = hb.add_temp_note(word)
            message = TextSendMessage(text=content)
            line_bot_api.reply_message(event.reply_token, message)



########### API範例 ##############################



# 建立一個名為 `tasks` 的資料表，用來儲存待辦事項
tasks = [
    {
        'title': 'Python程式設計備課',
        'description': '撰寫 API DEMO',
        'done': False

    },
    {
        'title': 'Pytest',
        'description': '增加程式單元測試',
        'done': False
    }
]


@app.route('/', methods=['GET'])
def helloworld():
    return "<h1>Hello World</h1>"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks':tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [ task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/tasks', methods=['POST'])
def add_task():
    # 取得使用者傳送的待辦事項
    task = request.json
    tasks.append(task)
    return jsonify({'tasks':tasks}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # 取得使用者傳送的更新資料
    task = request.json

    # 檢查待辦事項是否存在
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'message': 'task not found'}), 404

    # 更新待辦事項
    tasks[task_id] = task
    return jsonify({'message': f'task_id: {task_id} updated'}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # 檢查待辦事項是否存在
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({'message': 'task not found'}), 404

    # 刪除待辦事項
    tasks.pop(task_id)
    return jsonify({'message': 'task deleted'}), 200


#################################################

if __name__ == "__main__":
    app.run(port=5000, debug=True)