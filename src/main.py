from apscheduler.schedulers.blocking import BlockingScheduler
from tweet import tweet

sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True

@sched.scheduled_job('cron', id='tweet', minute='*/15')
def cron_tweet():
    tweet()
    
if __name__ == "__main__":
    sched.start()
