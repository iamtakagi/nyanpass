
from apscheduler.schedulers.blocking import BlockingScheduler

from Tweet import Tweet


# BlockingScheduler を初期化
scheduler = BlockingScheduler(daemon=True)

# 10分間隔でツイート
@scheduler.scheduled_job('cron', id='Tweet', minute='*/10')
def CronTweet():
    Tweet()

# スケジューリングを開始
# BlockingScheduler なのでここでブロッキングされる
scheduler.start()
