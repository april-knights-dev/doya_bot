import requests
import os
import json
TOKEN = os.environ['SLACK_API_TOKEN']
SLACK_CHANNEL_ID = 'CHKUSV4B1'
SLACK_URL = "https://slack.com/api/conversations.history"

def get_message():
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "token": TOKEN,
        "oldest":"1577849100",
        "latest":"1592796300"
    }
    response = requests.get(SLACK_URL, params=payload)
    json_data = response.json()
    print(json_data)
    messages = json_data["messages"]
    for i in messages:
        print(i["text"])

print(get_message())
