from .utility import SlackApi


def main_func():
    api = SlackApi()

    y, m = api.year(), api.month()
    begin, last = api.get_beginning_month(y, m), api.get_month_last(y, m)

    json_data = api.get_message(begin, last)
    messages = json_data.get("messages")

    if messages is None:
        return f"""
        みんなー、はむはー！！僕はDOYA太郎！
        残念ながら{m}月は誰もdoyaを呟いてくれなかったみたいなのだ

        今月はみんなdoyaを主張してくれると嬉しいのだ！
        それじゃあ、ばいきゅー
        """

    message_count = {}
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
    send_user = api.get_user(sorted_reactions[-1][0][1])  # 送信者のid
    send_message_link = api.get_permalink(ts)  # 投稿リンク
    sum_reaction = sorted_reactions[-1][1]  # リアクション数

    if not send_user:
        author_id = api.get_daikou_name(ts)
        send_user = api.get_user(author_id)
    else:
        send_user = f"{send_user}さん"

    message_format = f"""
    みんなー、はむはー！！僕はDOYA太郎！
    月間doya大賞の発表だよっ
    （※doya大賞の集計は毎月1日0:00〜月末23:59の投稿の中から集計しているのだ :star:）\n

    対象月：{m}月
    投稿者：{send_user}
    リアクション総数：{sum_reaction}個

    いちばんリアクションをもらった投稿なのだ
    {send_message_link}

　　来月もたくさんのdoyaをお待ちしているのだ！
    それじゃあ、ばいきゅー！
    """

    # print(message_format)
    return message_format
