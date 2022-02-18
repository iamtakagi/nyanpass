import os

from itsdangerous import json
from twitterApi import api

dest = 'data/timline_tweets.json'

def fetch_timeline_tweets():
    tweets = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
    f = open(dest, mode = 'r+')
    f.truncate(0)
    f.close()
    with open(dest, mode = "w") as file:
        file.write(tweets)

def get_tweets():
    with open(dest, "r") as file:
        tweets = json.load(file)
        return tweets