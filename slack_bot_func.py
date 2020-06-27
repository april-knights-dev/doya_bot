import os
import slack
from datetime import datetime
import datetime as dt
from apscheduler.schedulers.blocking import BlockingScheduler

import reaction_sum

# tokenの設定　環境変数に設定してる
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
sched = BlockingScheduler()

# ただメッセージを送るだけの関数
def send_message(channel, message):
    client.chat_postMessage(channel=channel, text=message)

# 本番用設定値 毎月12時00分00秒にtime_jobを実行
@sched.scheduled_job('cron', day=1, hour=12, minute=00, second=0)
# @sched.scheduled_job('cron', day=27, hour=16, minute=42, second=0)
def timed_job():
    message = reaction_sum.get_message()
    print(message)
    send_message('#tmp_bot放牧部屋', message)
    # channel_post('#tmp_bot放牧部屋', "テスト中")

# python slack_bot_func.py　で呼んだ時に実行される
if __name__ == "__main__":
    sched.print_jobs()
    send_message('#tmp_bot放牧部屋', "起動完了！")
    sched.start()
