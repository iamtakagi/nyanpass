import os
import logging
import MeCab
import tweepy
import re
import numpy as np
import json
from apscheduler.schedulers.blocking import BlockingScheduler

# Env
env = {
    "SCREEN_NAME": os.environ["SCREEN_NAME"],
    "CK": os.environ["CK"],
    "CS": os.environ["CS"],
    "AT": os.environ["AT"],
    "ATS": os.environ["ATS"]
}

# MeCab
mecab = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

# Templates
with open('./assets/templates.json', 'r') as json_file: 
    templates = json.load(json_file)

# Filter Words
with open('./assets/banned_words.json', 'r') as json_file:
    banned_words = json.load(json_file)

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
def filter_links(tweets):
    replyMatch = re.compile(r"@\w+")
    urlMatch = re.compile(r"https?://")
    data = []
    for text in tweets:
        if replyMatch.search(text) or urlMatch.search(text):
            continue
        data.append(text)
    return data

def filter_words(word):
    for w in banned_words:
        word = word.replace(w, '')
    return word

# 文章生成
def generate():
    # ツイート取得
    texts = [s.text for s in api.home_timeline(count = 100) if not s.user.screen_name == env["SCREEN_NAME"] and not s.retweeted and 'RT @' not in s.text]

    # フィルター
    data = filter_links(texts)
    for t in data:
        t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。") + ","

    # ツイートリストを出力
    logging.debug(data)
   
    # 名詞を格納するリスト
    nouns = []

    # 全ての文章から固有名詞だけを取り出す
    for text in data:
        t = text.replace(",", "")
        # 形態素出力
        logging.debug(mecab.parse(t))
        # 名詞を格納
        for n in [line for line in mecab.parse(t).splitlines() if "固有名詞" in line.split()[-1]]:
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

# フォロバ
@sched.scheduled_job('cron', id='follow_back', hour='*/1')
def follow_back():
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logging.debug(f"Following {follower.name}")
            follower.follow()

if __name__ == "__main__":
    # 起動時にフォロバ
    follow_back()
    # スケジューラ起動
    sched.start()
