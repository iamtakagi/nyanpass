
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from Tweet import Tweet


# ログの設定
logging.basicConfig(level=logging.INFO)

# BlockingScheduler を初期化
scheduler = BlockingScheduler(daemon=True)

# 10分間隔でツイート
@scheduler.scheduled_job('cron', id='tweet', minute='*/10')
def cron_tweet():
    Tweet()

# スケジューリングを開始
# BlockingScheduler なのでここでずっとブロッキングされる
scheduler.start()
