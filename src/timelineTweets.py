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
        file.write(json.dumps(api.home_timeline(count = 100)))

def get_tweets():
    tweets = []
    if not os.path.isfile(dest):
        return tweets
    with open(dest, "r") as file:
        json = json.load(file)
        tweets = [s.text for s in json if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
        return tweets