
import tweepy
import os


twitter_api = tweepy.API(tweepy.OAuth1UserHandler(
    os.environ['TWITTER_CK'], os.environ['TWITTER_CS'],
    os.environ['TWITTER_AT'], os.environ['TWITTER_ATS'],
))
