from makeTweetSentences import make_tweet_sentences
import numpy as np
from timelineTweets import fetch_timeline_tweets
from twitterApi import api 
from discordWebhook import send

def tweet():
    fetch_timeline_tweets()
    # 30%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,71) == 1:
        media = api.media_upload("assets/renge.gif")
        nyanpass_status = api.update_status(status = "にゃんぱすー", media_ids=[media.media_id])
        nyanpass_link = f'https://twitter.com/nyanpassnanon/status/{nyanpass_status.id}'
        send(nyanpass_link)
    sentence_1, sentence_2 = make_tweet_sentences()
    tweet_result_1 = api.update_status(status = sentence_1)
    tweet_result_2 = api.update_status(status = sentence_2)
    status_link_1 = f'https://twitter.com/nyanpassnanon/status/{tweet_result_1.id}'
    status_link_2 = f'https://twitter.com/nyanpassnanon/status/{tweet_result_2.id}'
    send(status_link_1)
    send(status_link_2)

