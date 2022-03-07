import os

import json
from twitterApi import api

dest = 'data/timeline_tweets.json'

def fetch_timeline_tweets():
    if os.path.isfile(dest):
        with open(dest, mode = 'r+') as current:
            current.truncate(0)
            current.close()
    with open(dest, mode = "w") as file:
        tweets = [s.text for s in api.home_timeline(count = 200) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text and "http" not in s.text]
        file.write(json.dumps(tweets))

def get_tweets():
    if not os.path.isfile(dest):
        return []
    with open(dest, "r") as file:
        return json.load(file)
