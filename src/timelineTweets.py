import os

import json
from twitterApi import api

dest = 'data/timline_tweets.json'

def fetch_timeline_tweets():
    tweets = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
    if os.path.isfile("data/home_timeline.json"):
        with open(dest, mode = 'r+') as current:
            current.truncate(0)
            current.close()
    with open(dest, mode = "w") as file:
        file.write(tweets)

def get_tweets():
    tweets = []
    if not os.path.isfile("data/home_timeline.json"):
        return tweets
    with open(dest, "r") as file:
        json = json.load(file)
        tweets = [s.text for s in json if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
        return tweets