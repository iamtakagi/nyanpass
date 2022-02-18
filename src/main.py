from apscheduler.schedulers.blocking import BlockingScheduler
from makeSentences import make_sentences
from timelineTweets import fetch_timeline_tweets, get_tweets
from tweet import tweet
import logging
from replyStream import ReplyStreamListener, ReplyStream
from twitterAuth import auth
import os

logging.basicConfig(level=logging.DEBUG)

sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True


@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()


@sched.scheduled_job('interval', id='reply_stream', seconds=60)
def reply_stream():
    listener = ReplyStreamListener()
    stream = ReplyStream(auth, listener)
    stream.start()


if __name__ == "__main__":
    sched.start()