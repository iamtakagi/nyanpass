import os
import urllib
from makeSentences import make_sentences
import numpy as np
from timelineTweets import fetch_timeline_tweets
from twitterApi import api 
from discordWebhook import post_discord_webhook

def tweet():
    fetch_timeline_tweets()
    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        media = api.media_upload("renge.gif")
        nyanpass_status = api.update_status(status = "にゃんぱすー", media_ids=[media.media_id])
        nyanpass_link = f'https://twitter.com/{os.environ["SCREEN_NAME"]}/status/{nyanpass_status.id}'
        post_discord_webhook(nyanpass_link)
    sentence_1, sentence_2 = make_sentences()
    tweet_result_1 = api.update_status(status = sentence_1)
    tweet_result_2 = api.update_status(status = sentence_2)
    status_link_1 = f'https://twitter.com/{os.environ["SCREEN_NAME"]}/status/{tweet_result_1.id}'
    status_link_2 = f'https://twitter.com/{os.environ["SCREEN_NAME"]}/status/{tweet_result_2.id}'
    post_discord_webhook(status_link_1)
    post_discord_webhook(status_link_2)

