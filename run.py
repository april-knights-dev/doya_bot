# coding: utf-8
import os
from threading import Thread

import slack
from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

from plugins.reaction_sum import get_message


sched = BlockingScheduler()


@sched.scheduled_job("cron", day=1, hour=12, minute=0, second=0)
def timed_job():
    message = get_message()
    send_message("G0149FE9SAW", message)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print("start slackbot")

    # RTMbotの起動
    job = Thread(target=main)
    job.start()

    # APSchedulerの起動
    job = Thread(target=sched.start)
    job.start()
