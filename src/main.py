
import logging
from apscheduler.schedulers.background import BackgroundScheduler

from Tweet import Tweet


# ロギング
logging.basicConfig(level=logging.DEBUG)

# BackgroundScheduler を初期化
sched = BackgroundScheduler(daemon=True)

# 15分間隔でツイート
@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    Tweet()

# スケジューリングを開始
sched.start()
