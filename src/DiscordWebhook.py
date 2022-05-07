
import json
import os
import requests


def SendDiscord(text: str):
    """
    Discord Webhook にメッセージを送信する

    Args:
        text (str): 送信するメッセージ
    """

    requests.post(
        os.environ['DISCORD_WEBHOOK_URL'],
        json.dumps({'content': text}),
        headers = {'Content-Type': 'application/json'},
    )
