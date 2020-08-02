# coding: utf-8
import slack
from slackbot.bot import respond_to
import os

from .reaction_sum import get_user, get_permalink

# @botname: で反応するデコーダ

# tokenの設定　環境変数に設定してる
client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

# from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
# from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない


# メッセージ送る
def send_message(channel, message):
    print("呼ばれた")
    client.chat_postMessage(channel=channel, text=message)


# メンション+メッセージを受ける（メッセージが空だとデフォルト返答をする）
@respond_to(r".+")
def mention_func(message):
    body = message.body
    link = get_permalink(body["channel"], body["ts"])
    name = get_user(body["user"])
    send_message("CHKUSV4B1", f"【doya代行】\n{name}さん、偉いのだ！\n\n{link}")
    print("doya部屋へ送信完了")
