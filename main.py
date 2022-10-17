from apscheduler.schedulers.background import BackgroundScheduler
from makeSentences import make_sentences
from timelineTweets import fetch_timeline_tweets, get_tweets
from tweet import tweet
import logging
from replyStream import ReplyStream
from twitterAuth import auth
from flask_cors import CORS
from flask import Flask, render_template, jsonify
import os
import numpy as np

logging.basicConfig(level=logging.DEBUG)

scheduler = BackgroundScheduler(daemon=True)

# 10分毎にツイート
@scheduler.scheduled_job('cron', id='tweet', minute='*/10')
def cron_tweet():
    tweet()


app = Flask(__name__)
CORS(app)

@app.get("/api/make_sentence")
def make_sentence():
    # 10%の確率で「にゃんぱすー」を返す
    if np.random.randint(1, 91) == 1:
        return jsonify({'sentence': 'にゃんぱすー'})
    if not get_tweets():
        fetch_timeline_tweets()
    sentence_1, sentence_2 = make_sentences()
    return jsonify({'sentence': sentence_1})


# 返信ストリーム
replyStream: ReplyStream or None = None

def initReplyStream():
    global replyStream
    # 接続
    replyStream = ReplyStream(
        os.environ['TWITTER_CK'], os.environ['TWITTER_CS'],
        os.environ['TWITTER_AT'], os.environ['TWITTER_ATS'],
    )
    if replyStream is not None:
        replyStream.filter(
            track=[f'@{os.environ["SCREEN_NAME"]}'], threaded=True)


def reconnectReplyStream():
    if replyStream is not None:
        # 再接続
        replyStream.disconnect()
        replyStream.filter(
            track=[f'@{os.environ["SCREEN_NAME"]}'], threaded=True)
       

# 1時間毎に返信ストリーム再接続
@scheduler.scheduled_job('cron', id='restart_stream', minute='*/57')
def cron_restart_stream():
    reconnectReplyStream()


# 返信ストリーム初期化
initReplyStream()

# スケジューラ起動
scheduler.start()

if __name__ == "__main__":
    app.run(
        threaded=True,
        host=os.environ["HOST"],
        debug=False
    )
