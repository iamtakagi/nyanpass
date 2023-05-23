
from apscheduler.schedulers.blocking import BlockingScheduler

from Tweet import OnAirNotificationTweet, Tweet


# BlockingScheduler を初期化
scheduler = BlockingScheduler(daemon=True)

# 10分間隔でツイート
@scheduler.scheduled_job('cron', id='Tweet', minute='*/10')
def CronTweet():
    Tweet()

# 毎週土曜日の22:55にツイート (テレビ東京)
@scheduler.scheduled_job('cron', id='TVTokyoOnAirTweet', day_of_week='sat', hour=22, minute=55)
def CronTVTokyoOnAirTweet():
    OnAirNotificationTweet('#tvtokyo')

# 毎週月曜日の00:30にツイート (BSテレ東)
@scheduler.scheduled_job('cron', id='BSTVTokyoOnAirTweet', day_of_week='mon', hour=0, minute=30)
def CronBSTVTokyoOnAirTweet():
    OnAirNotificationTweet('#bstvtokyo')

# スケジューリングを開始
# BlockingScheduler なのでここでブロッキングされる
scheduler.start()
