import os
import logging
import MeCab
import tweepy
import re
import json
from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask, jsonify, request

from makeSentences import make_sentences

# Flask
app = Flask(__name__)

# CORS
from flask_cors import CORS
CORS(app)

# Logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/api/sentence")
def sentence():
    sentence_1, sentence_2 = make_sentences()
    return jsonify({'sentence_1': sentence_1, 'sentence_2': sentence_2})

if __name__ == "__main__":
    app.run (
          threaded=True,
          host = os.environ["HOST"], 
          port = os.environ["PORT"], 
          debug = True
    )