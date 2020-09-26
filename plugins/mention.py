# coding: utf-8
import slack
from slackbot.bot import respond_to
import os

from .utility import SlackApi

api = SlackApi()

# tokenの設定　環境変数に設定してる
client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])


# メッセージ送る
def send_message(channel, message):
    print("呼ばれた")
    client.chat_postMessage(channel=channel, text=message)


# メンション+メッセージを受ける（メッセージが空だとデフォルト返答をする）
@respond_to(r".+")
def mention_func(message):
    body = message.body
    link = api.get_permalink(body["channel"], body["ts"])
    name = api.get_user(body["user"])
    send_message(api.SLACK_CHANNEL_ID, f"【doya代行】\n{name}さん、偉いのだ！\n\n{link}")
    print("doya部屋へ送信完了")
