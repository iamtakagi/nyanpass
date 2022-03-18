import random
import MeCab
import numpy as np
from choiceRandomNoun import choiceRandomNoun

from makeSentences import make_sentences
from timelineTweets import get_tweets, fetch_timeline_tweets
from filters import normalize_text
import re


"""
おみくじ 確率
大吉=1% (0.01)
中吉=9% (0.09)
小吉=10% (0.1)
吉=60% (0.6)
末吉=10% (0.1)
凶=10% (0.1)
"""
def omikuji(screen_name):
    return "@{} {}なん！ラッキーワードは「{}」なのん！".format(screen_name, np.random.choice(["大吉", "中吉", "小吉", "吉", "末吉", "凶"], p=[0.01, 0.09, 0.1, 0.6, 0.1, 0.1]), choiceRandomNoun())

def janken(screen_name, text):
    result = random.choice(("グー✊", "チョキ✌", "パー✋"))
    text = text.replace("ぐー", "グー").replace("ちょき", "チョキ").replace("ぱー", "パー").replace("✊", "グー").replace("👊", "グー").replace("✌", "チョキ").replace("✋", "パー")
    janken = ""
    # あいこ
    if result in text: 
        janken = "@{} {}なん！あいこなん！".format(screen_name, result)
    # 勝ちパターン
    if result == "グー" and "チョキ" in text or result == "チョキ" and "パー" in text or result == "パー" and "グー" in text:
        janken = "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
    # 負けパターン
    if result == "グー" and "パー" in text or result == "チョキ" and "グー" in text or result == "パー" and "チョキ" in text:
        janken = "@{} {}なん！うちの負けなん！".format(screen_name, result)
    return janken

def make_reply_sentence(status):
    screen_name = status.user.screen_name
    text = normalize_text(status.text)
    text = text.replace(",", "").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace('@nyanpassnanon', "")
    # にゃんぱすー
    if "にゃんぱす" in text:
        return "@{} にゃんぱすー".format(screen_name)
    # 占い
    if re.compile(r"(?:うらな(?:って|い)|占(?:って|い)|おみくじ|運勢?)").search(text):
        if not get_tweets():
            fetch_timeline_tweets()
        return omikuji(screen_name)
    # じゃんけん
    if re.compile(r"(?:[✊✋✌👊]|[ぐぱグパ]ー|ちょき|チョキ)").search(text):
        return janken(screen_name, text)
    if text:
         # 10%の確率で「にゃんぱすー」を返す
        if np.random.randint(1,91) == 1:
            return "@{} にゃんぱすー".format(screen_name)
        if not get_tweets():
            fetch_timeline_tweets()
        sentence_1, sentence_2 = make_sentences() 
        return "@{} {}".format(screen_name, sentence_1)
    return None