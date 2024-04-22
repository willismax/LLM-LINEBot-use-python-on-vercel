from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
import openai

app = Flask(__name__)

# Configuration for the LINE Bot API
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

openai_api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")  # Optional, if your API key is associated with an organization

@app.route('/')
def home():
    return '<h1>Hello World</h1>'

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "This is a Linebot conversation."},
                  {"role": "user", "content": user_message}],
        api_key=openai_api_key
    )
    reply_text = gpt_response.get("choices")[0].get("message").get("content")

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        response = line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )
    app.logger.info("Response: " + str(response.data))

if __name__ == "__main__":
    app.run()
