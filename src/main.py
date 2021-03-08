import os
import logging
import MeCab
import tweepy
import re
import random

# MeCab
mecab = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

# Env
env = {"SCREEN_NAME": os.environ["SCREEN_NAME"], "CK": os.environ["CK"], "CS": os.environ["CS"], "AT": os.environ["AT"], "ATS": os.environ["ATS"]}

# 語幹・語尾セットリスト
sets = [
        {"gokan": "", "gobi": "なのん"},
        {"gokan": "", "gobi": "やるん"},
        {"gokan": "うちは", "gobi": ""},
        {"gokan": "うちも", "gobi": "やるん"},
        {"gokan": "うちも", "gobi": "やるのん"},
        {"gokan": "うちも", "gobi": "やりたいのん"},
        {"gokan": "うち、", "gobi": "は嫌いじゃないのん。"},
        {"gokan": "", "gobi": " 知らなかったん。ありがとなーん。"},
        {"gokan": "暇を持て余してるからって、", "gobi": "で遊ばないでほしいのんな"},
        {"gokan": "そんな所で寝たら、", "gobi": "にくわれるん。うぁ……もう、手遅れなんな…。"},
        {"gokan": "うち、", "gobi": "の代わりなのん？　…頑張るん！"},
        {"gokan": "こまちゃんの", "gobi": "かわいいのんな。"},
        {"gokan": "こいつの名前は", "gobi": "にするのん"},
        {"gokan": "ほたるん", "gobi": "なのん?"},
        {"gokan": "ほたるんにうちの", "gobi": "見せるのん!"},
        {"gokan": "うちは", "gobi": "だから楽しいのん"},
        {"gokan": "なっつん!", "gobi": "食べよ!"}
]


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
    texts = []
    for status in api.home_timeline(count = 50):
        texts.append(status.text)

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
        print(mecab.parse(t))
        nouns = [line for line in mecab.parse(t).splitlines() if "固有名詞" in line.split()[-1]]
        for n in nouns:
            meisi_list.append(n.split("\t")[0])

    # 名詞リストを出力
    logging.debug(meisi_list)

    # ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章にする
    s = random.choice(sets)
    sentence = s["gokan"] + random.choice(meisi_list) + s["gobi"]
    return sentence

# ツイート
def tweet():
    sentence = generate()
    api.update_status(status = sentence)
    
if __name__ == "__main__":
    tweet()
