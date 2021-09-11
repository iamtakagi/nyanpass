import tweepy
from makeSentences import make_sentences
import numpy as np
from twitterApi import api 
from discordWebhook import send

def tweet():
    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        nyanpass_status = api.update_status(status = "にゃんぱすー")
        nyanpass_link = f'https://twitter.com/nyanpassnanon/status/{nyanpass_status.id}'
        send(nyanpass_link)
    sentence_1, sentence_2 = make_sentences()
    tweet_result_1 = api.update_status(status = sentence_1)
    tweet_result_2 = api.update_status(status = sentence_2)
    status_link_1 = f'https://twitter.com/nyanpassnanon/status/{tweet_result_1.id}'
    status_link_2 = f'https://twitter.com/nyanpassnanon/status/{tweet_result_2.id}'
    send(status_link_1)
    send(status_link_2)

