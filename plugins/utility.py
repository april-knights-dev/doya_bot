import os
import calendar
import requests
from datetime import datetime


class SlackApi:
    def __init__(self):
        self.TOKEN = os.environ["SLACK_API_TOKEN"]
        self.SLACK_CHANNEL_ID = "CHKUSV4B1"

    def year(self):
        return datetime.now().year

    def month(self):
        return datetime.now().month - 1

    # 過去の投稿を取得
    def get_message(self, begin, last):
        SLACK_URL = "https://slack.com/api/conversations.history"

        payload = {
            "channel": self.SLACK_CHANNEL_ID,
            "token": self.TOKEN,
            "oldest": begin,  # 前月の月初
            "latest": last,  # 前月の月末
        }

        response = requests.get(SLACK_URL, params=payload)
        json_data = response.json()
        # pprint(json_data)

        return json_data

    # 投稿のリンクを取得
    def get_permalink(self, ts):
        SLACK_URL = "https://slack.com/api/chat.getPermalink"
        payload = {
            "channel": self.SLACK_CHANNEL_ID,
            "token": self.TOKEN,
            "message_ts": ts,
        }
        response = requests.get(SLACK_URL, params=payload)
        json_data = response.json()

        return json_data.get("permalink")

    # ユーザIDからユーザの表示名を取得
    def get_user(self, user_id):

        SLACK_URL = "https://slack.com/api/users.info"
        payload = {
            "token": self.TOKEN,
            "user": user_id,
        }
        response = requests.get(SLACK_URL, params=payload)
        json_data = response.json()

        return json_data["user"]["profile"]["display_name"]

    def get_beginning_month(self, y, m):
        unix_beginning_month = datetime.strptime(
            f"{y}/{m}/01 00:00:00", "%Y/%m/%d %H:%M:%S"
        ).timestamp()

        return unix_beginning_month

    def get_month_last(self, y, m):
        _, days = calendar.monthrange(y, m)
        end_month = datetime.strptime(
            f"{y}/{m}/{days} 23:59:59", "%Y/%m/%d %H:%M:%S"
        ).timestamp()

        return end_month

    def get_daikou_name(self, ts):
        daikou_message = self.get_message(float(ts) - 1.0, float(ts) + 1.0)
        author_id = (
            daikou_message.get("messages")[0].get("attachments")[0].get("author_id")
        )
        return author_id
