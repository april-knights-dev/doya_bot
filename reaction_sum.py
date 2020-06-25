import requests
import os
import json
import pprint

# TOKEN = os.environ['SLACK_API_TOKEN']
TOKEN = "xoxb-331326118613-1132985285975-v2OMvs9sQ4RmG0rkSRsDk6jL"
SLACK_CHANNEL_ID = 'CHKUSV4B1'

# 投稿のリンクを取得
def get_permalink(ts):
    SLACK_URL = "https://slack.com/api/chat.getPermalink"
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN,
        "message_ts": ts
    }
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

# 過去の投稿を取ってきてあーだこーだしてる
def get_message():
    SLACK_URL = "https://slack.com/api/conversations.history"
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN,
        # "oldest":"1577849100",
        # "latest":"1592796300"
    }
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    # print(json_data)

    message_count = {}
    messages = json_data["messages"]
    for data in messages:
        if data.get("reactions"):
            # print(data.get("user"))
            # print(data.get("text"))

            reactions = []
            for count in data.get("reactions"):

                reactions.append(count.get("count"))
            # print(sum(reactions))

            # {"userid": リアクションの合計数}みたいなdictを作成中
            message_count[data.get("ts"),
                       data.get("user")] = sum(reactions)

    # dictをリアクションのカウント数でソート
    sorted_reactions = sorted(message_count.items(), key=lambda x: x[1])
    # pprint.pprint(sorted_reactions)


    ts = sorted_reactions[-1][0][0] # timestamp(unixtime)
    # print("userid", type(sorted_reactions[-1][0][1]))
    send_user = get_user(sorted_reactions[-1][0][1])  # 送信者のid
    send_message_link = get_permalink(ts) # 投稿リンク
    sum_reaction = sorted_reactions[-1][1]  # リアクション数
    
    # for data in messages:
    #     if data.get("client_msg_id") == send_id:
    #         send_text = data.get("text")

    message_format = f"""
    みんなー、はむはー！！僕はDOYA太郎！
    月間doya大賞の発表だよっ
    （※doya大賞の集計は毎月1日0:00〜月末23:59の投稿の中から集計しているのだ :star:）\n

    投稿者：{send_user}さん
    リアクション総数：{sum_reaction}個

    いちばんリアクションをもらった投稿なのだ
    {send_message_link}

    それじゃあ、ばいきゅー
    """

    print(message_format)
    return message_format
        # for i in messages:
    #     print(i["text"])

