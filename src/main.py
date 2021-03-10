import os
import logging
import MeCab
import tweepy
import re
import numpy as np
import json
from apscheduler.schedulers.blocking import BlockingScheduler

# Env
env = {"SCREEN_NAME": os.environ["SCREEN_NAME"], "CK": os.environ["CK"], "CS": os.environ["CS"], "AT": os.environ["AT"], "ATS": os.environ["ATS"]}

# MeCab
mecab = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

# Sets
with open('./assets/sets.json') as json_file: 
    sets = json.load(json_file)

# Logging
logging.basicConfig(level=logging.DEBUG)

sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True

# Tweepy
auth = tweepy.OAuthHandler(env["CK"], env["CS"])
auth.set_access_token(env["AT"], env["ATS"])
api = tweepy.API(auth)

# Reply URL フィルター
def filter(tweets):
    replyMatch = re.compile(r"@\w+")
    urlMatch = re.compile(r"https?://")
    data = []
    for text in tweets:
        if replyMatch.search(text) or urlMatch.search(text):
            continue
        data.append(text)
    return data

# 文章生成
def generate():
    # ツイート取得
    texts = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == env["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]

    # フィルター
    data = filter(texts)

    for t in data:
        t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。") + ","

    # ツイートリストを出力
    logging.debug(data)
   
    # 名詞を格納するリスト
    meisi_list = []

    # 全ての文章から固有名詞だけを取り出す
    for text in data:
        t = text.replace(",", "")
        logging.debug(mecab.parse(t))
        nouns = [line for line in mecab.parse(t).splitlines() if "固有名詞" in line.split()[-1]]
        for n in nouns:
            meisi_list.append(n.split("\t")[0])

    # 名詞リストを出力
    logging.debug(meisi_list)

    # ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を2つ生成する
    s_1 = np.random.choice(sets)
    s_2 = np.random.choice(sets)
    sentence_1 = s_1["gokan"] + np.random.choice(meisi_list) + s_1["gobi"]
    sentence_2 = s_2["gokan"] + np.random.choice(meisi_list) + s_2["gobi"]

    # 文章を出力
    logging.debug(sentence_1)
    logging.debug(sentence_2)

    # 文章を返す
    return sentence_1, sentence_2

# ツイート
@sched.scheduled_job('cron', id='tweet', minute='*/15')
def tweet():
    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        api.update_status(status = "にゃんぱすー")
    sentence_1, sentence_2 = generate()
    api.update_status(status = sentence_1)
    api.update_status(status = sentence_2)
    
if __name__ == "__main__":
    sched.start()