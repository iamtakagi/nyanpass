import tweepy
from makeSentences import make_sentences
import numpy as np
from twitterApi import api 

def tweet():
    exportTweets()

    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        api.update_status(status = "にゃんぱすー")
        sentence_1, sentence_2 = make_sentences()
        api.update_status(status = sentence_1)
        api.update_status(status = sentence_2)

if __name__ == '__main__':
    tweet()
