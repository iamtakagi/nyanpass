import os

from itsdangerous import json
from twitterApi import api

def fetch_timeline_tweets():
    tweets = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
    with open('data/timline_tweets.json', mode = "w") as file:
        file.write(tweets)

def get_tweets():
    with open('data/timline_tweets.json', "r") as file:
        tweets = json.load(file)
        return tweets