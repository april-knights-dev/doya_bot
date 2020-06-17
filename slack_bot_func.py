import os
import slack
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# tokenの設定　環境変数に設定してる
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
# sched = BlockingScheduler()

# ただメッセージを送るだけの関数
# APScadulerなしだとこのslack_bot_func.pyを実行した時に1回呼ばれる
def send_message(channel, message):
    client.chat_postMessage(channel=channel, text=message)


# 前回timezoneでやられたので次使う時は設定したい
# @sched.scheduled_job('date', run_date='2020-05-28 13:15:00')
# def timed_job():
#     channel_post('#tmp_bot放牧部屋', "テスト中")

# sched.start()

# python slack_bot_func.py　で呼んだ時に実行される
if __name__ == "__main__":
    send_message('#tmp_bot放牧部屋', "我はdoya神")
