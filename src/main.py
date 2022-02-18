from apscheduler.schedulers.blocking import BlockingScheduler
from tweet import tweet
import logging
from replyStream import ReplyStreamListener, ReplyStream
from twitterAuth import auth

logging.basicConfig(level=logging.DEBUG)

sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True

@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()

@sched.scheduled_job('interval', id='reply_stream' seconds=15)　
def reply_stream():
　　 listener = ReplyStreamListener()
    stream = ReplyStream(auth, listener)
    stream.start()

if __name__ == "__main__":
    sched.start()
