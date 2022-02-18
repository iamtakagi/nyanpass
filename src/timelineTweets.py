from twitterApi import api
import os

tweets = []

def fetch_timeline_tweets():
    global tweets
    tweets = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]