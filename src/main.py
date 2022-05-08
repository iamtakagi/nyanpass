from apscheduler.schedulers.background import BackgroundScheduler
from makeSentences import make_sentences
from timelineTweets import fetch_timeline_tweets, get_tweets
from tweet import tweet
import logging
from replyStream import ReplyStreamListener, ReplyStream
from twitterAuth import auth
from flask_cors import CORS
from flask import Flask, jsonify
import os
import numpy as np

logging.basicConfig(level=logging.DEBUG)

sched = BackgroundScheduler(daemon=True)

@sched.scheduled_job('cron', id='tweet', minute='*/10')
def cron_tweet():
    tweet()


@sched.scheduled_job('interval', id='reply_stream', seconds=60)
def reply_stream():
    listener = ReplyStreamListener()
    stream = ReplyStream(auth, listener)
    stream.start()

sched.start()
app = Flask(__name__)
CORS(app)

@app.get("/api/make_sentence")
def make_sentence():
    # 10%の確率で「にゃんぱすー」を返す
    if np.random.randint(1,91) == 1:
        return jsonify({'sentence': 'にゃんぱすー'})
    if not get_tweets():
        fetch_timeline_tweets()
    sentence_1, sentence_2 = make_sentences()
    return jsonify({'sentence': sentence_1})
    

app.run (
    threaded=True,
    host = os.environ["HOST"], 
    port = os.environ["PORT"], 
    debug=False
)
