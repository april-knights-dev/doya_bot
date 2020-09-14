import requests
import os
from datetime import datetime
import calendar
from pprint import pprint

TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_CHANNEL_ID = "CHKUSV4B1"


# 投稿のリンクを取得
def get_permalink(channel_id, ts):
    SLACK_URL = "https://slack.com/api/chat.getPermalink"
    payload = {"channel": channel_id, "token": TOKEN, "message_ts": ts}
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    # print(json_data)
    return json_data.get("permalink")


# ユーザIDからユーザの表示名を取得
def get_user(user_id):

    SLACK_URL = "https://slack.com/api/users.info"
    payload = {
        "token": TOKEN,
        "user": user_id,
    }
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()

    print(json_data)

    # return "test"
    return json_data["user"]["profile"]["display_name"]


def get_beginning_month(y, m):
    unix_beginning_month = datetime.strptime(
        f"{y}/{m}/01 00:00:00", "%Y/%m/%d %H:%M:%S"
    ).timestamp()
    return unix_beginning_month


def get_month_last(y, m):
    _, days = calendar.monthrange(y, m)
    end_month = datetime.strptime(
        f"{y}/{m}/{days} 23:59:59", "%Y/%m/%d %H:%M:%S"
    ).timestamp()
    return end_month


# 過去の投稿を取ってきてあーだこーだしてる
def get_message():
    SLACK_URL = "https://slack.com/api/conversations.history"

    year = datetime.now().year
    month = datetime.now().month - 1

    print(datetime.fromtimestamp(get_beginning_month(year, month)))
    print(datetime.fromtimestamp(get_month_last(year, month)))

    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN,
        "oldest": get_beginning_month(year, month),  # 前月の月初
        "latest": get_month_last(year, month),  # 前月の月末
    }

    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()  # 最初からdictだった
    pprint(json_data)
    # print(json_data)

    message_count = {}
    messages = json_data.get("messages")

    if messages is None:
        return f"""
        みんなー、はむはー！！僕はDOYA太郎！
        残念ながら{month}月は誰もdoyaを呟いてくれなかったみたいなのだ

        今月はみんなdoyaを主張してくれると嬉しいのだ！
        それじゃあ、ばいきゅー
        """

    for data in messages:
        if data.get("reactions"):

            reactions = []
            for count in data.get("reactions"):
                reactions.append(count.get("count"))

            # {(ts, "userid") : リアクションの合計数 } みたいなdictを作成中
            message_count[data.get("ts"), data.get("user")] = sum(reactions)

    # dictをリアクションのカウント数でソート
    sorted_reactions = sorted(message_count.items(), key=lambda x: x[1])

    ts = sorted_reactions[-1][0][0]  # timestamp(unixtime)
    send_user = get_user(sorted_reactions[-1][0][1])  # 送信者のid
    send_message_link = get_permalink(SLACK_CHANNEL_ID, ts)  # 投稿リンク
    sum_reaction = sorted_reactions[-1][1]  # リアクション数

    if not send_user:
        send_user = "代行"
    else:
        send_user = f"{send_user}さん" 

    message_format = f"""
    みんなー、はむはー！！僕はDOYA太郎！
    月間doya大賞の発表だよっ
    （※doya大賞の集計は毎月1日0:00〜月末23:59の投稿の中から集計しているのだ :star:）\n

    対象月：{month}月
    投稿者：{send_user}
    リアクション総数：{sum_reaction}個

    いちばんリアクションをもらった投稿なのだ
    {send_message_link}

　　来月もたくさんのdoyaをお待ちしているのだ！
    それじゃあ、ばいきゅー！
    """

    print(message_format)
    return message_format
