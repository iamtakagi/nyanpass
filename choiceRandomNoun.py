import logging
import json
import MeCab
from filters import filter_words, filter_links
import numpy as np
from twitterApi import api
from templates import templates
from timelineTweets import get_tweets
import os

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def choiceRandomNoun():
    tweets = get_tweets()
    # フィルター
    data = filter_links(tweets)
    for t in data:
        t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。") + ","

    # ツイートリストを出力
    logging.debug(data)

    # 名詞を格納するリスト
    nouns = []

    # 全ての文章から固有名詞だけを取り出す
    for tweet in data:
        t = tweet.replace(",", "")
        parsed = mecab.parse(t)
        # 形態素出力
        logging.debug(parsed)
        # 名詞を格納
        for n in [line for line in parsed.splitlines() if "固有名詞" in line.split()[-1]]:
            noun = n.split("\t")[0]
            # 重複チェック
            if not noun in nouns:
                nouns.append(noun)

    return filter_words(np.random.choice(nouns))