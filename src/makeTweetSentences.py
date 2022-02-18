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

def make_tweet_sentences():
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

    # 名詞リストを出力
    logging.debug(nouns)

    # ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を2つ生成する
    s_1 = np.random.choice(templates)
    s_2 = np.random.choice(templates)
    n_1 = filter_words(np.random.choice(nouns))
    n_2 = filter_words(np.random.choice(nouns))
    sentence_1 = s_1["gokan"] + n_1 + s_1["gobi"]
    sentence_2 = s_2["gokan"] + n_2 + s_2["gobi"]

    # 文章を返す
    return sentence_1, sentence_2
