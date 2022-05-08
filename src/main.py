
import logging
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from ReplyStream import ReplyStream
from Tweet import Tweet
from TwitterAPI import twitter_auth


# ログの設定
logging.basicConfig(level=logging.INFO)

# BlockingScheduler を初期化
scheduler = BlockingScheduler(daemon=True)

# 10分間隔でツイート
@scheduler.scheduled_job('cron', id='tweet', minute='*/10')
def cron_tweet():
    Tweet()

# 1分間隔でリプライを返す
@scheduler.scheduled_job('interval', id='reply_stream', seconds=60)
def reply_stream():
    stream = ReplyStream(auth=twitter_auth, tweet_mode='extended')
    stream.filter(track=[f'@{os.environ["SCREEN_NAME"]}'])

# スケジューリングを開始
# BlockingScheduler なので終了までここでずっとブロッキングされる
scheduler.start()
