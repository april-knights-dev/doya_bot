from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os


def get_spread_data():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    json_file = "sample.json"  # OAuth用クライアントIDの作成でダウンロードしたjsonファイル
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        json_file, scopes=scopes
    )
    # http_auth = credentials.authorize(Http()) # 出番忘れた、消すかも

    # スプレッドシート用クライアントの準備
    doc_id = os.environ[
        "DOC_ID"
    ]  # これはスプレッドシートのURLのうちhttps://docs.google.com/spreadsheets/d/以下の部分
    client = gspread.authorize(credentials)
    gfile = client.open_by_key(doc_id)  # 読み書きするgoogle spreadsheet
    worksheet = gfile.sheet1  # ここシート名に多分なるんだけどちょっと考える

    # それぞれ称号名とリアクションを取得
    title_list = worksheet.col_values(1)
    reaction_list = worksheet.col_values(2)

    # 称号名と称号に対応したリアクションのセットをdictとして作る
    title_set = dict(zip(title_list, reaction_list))
    print(title_set)

    return title_set
