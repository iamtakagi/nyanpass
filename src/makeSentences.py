import logging
import json
import MeCab
from choiceRandomNoun import choiceRandomNoun
from filters import filter_words, filter_links
import numpy as np
from twitterApi import api
from templates import templates
from timelineTweets import get_tweets
import os

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def make_sentences():
    # ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を2つ生成する
    s_1 = np.random.choice(templates)
    s_2 = np.random.choice(templates)
    sentence_1 = s_1["gokan"] + choiceRandomNoun() + s_1["gobi"]
    sentence_2 = s_2["gokan"] + choiceRandomNoun() + s_2["gobi"]

    # 文章を返す
    return sentence_1, sentence_2
