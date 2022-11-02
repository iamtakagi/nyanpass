import os
import urllib
from makeSentences import make_sentences
import numpy as np
from timelineTweets import fetch_timeline_tweets
from twitterApi import api 

def tweet():
    fetch_timeline_tweets()
    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        media = api.media_upload("renge.gif")
        api.update_status(status = "にゃんぱすー", media_ids=[media.media_id])
    sentence_1, sentence_2 = make_sentences()
    api.update_status(status = sentence_1)
    api.update_status(status = sentence_2)

