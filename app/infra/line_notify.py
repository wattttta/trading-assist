from linebot import LineBotApi
from linebot.models import TextSendMessage

def send_line_message(token: str, message: str):
    line_bot_api = LineBotApi(token)
    line_bot_api.broadcast(TextSendMessage(text=message))