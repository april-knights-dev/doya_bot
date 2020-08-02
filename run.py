# coding: utf-8
from threading import Thread

from slackbot.bot import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

from plugins.reaction_sum import get_message
from plugins.mention import send_message

sched = BlockingScheduler()


@sched.scheduled_job("cron", day="1st mon", hour=12, minute=0, second=0)
# @sched.scheduled_job("cron", day=2, hour=1, minute=40, second=0)
def timed_job():
    message = get_message()
    send_message("CA798CMV0", message)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print("start slackbot")

    # RTMbotの起動
    job = Thread(target=main)
    job.start()
    print("RTMbot job start")

    # APSchedulerの起動
    job = Thread(target=sched.start)
    job.start()
    print("APScheduler job start")
