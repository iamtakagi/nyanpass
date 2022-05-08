
import logging
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from ReplyStream import ReplyStream
from Tweet import Tweet


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
    stream = ReplyStream(
        os.environ['TWITTER_CK'], os.environ['TWITTER_CS'],
        os.environ['TWITTER_AT'], os.environ['TWITTER_ATS'],
    )
    stream.filter(track=[f'@{os.environ["SCREEN_NAME"]}'])

# スケジューリングを開始
# BlockingScheduler なので終了までここでずっとブロッキングされる
scheduler.start()
