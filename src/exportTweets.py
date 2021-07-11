import json
import os
from filters import filter_links
from twitterApi import api

def exportTweets():
    tweets = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == os.environ["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]
    tweets = filter_links(tweets)

    for t in tweets:
        t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。") + ","

    with open("tweets.json", "w") as f:
        f.write(json.dumps(tweets))

if __name__ == '__main__':
    exportTweets()
