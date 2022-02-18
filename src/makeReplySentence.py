import random
import MeCab
import numpy as np

from makeTweetSentences import make_tweet_sentences
from timelineTweets import get_tweets, fetch_timeline_tweets
from filters import normalize_text

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def make_reply_sentence(status):
    screen_name = status.user.screen_name
    text = normalize_text(text)
    text = text.replace(",", "").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。").replace('@nyanpassnanon', "")
    # 占い
    if "占って" in text or "うらなって" in text or "おみくじ" in text:
        return "@{} {}なん！".format(screen_name, random.choice(("凶", "大凶", "末吉", "吉", "小吉", "中吉", "大吉")))
    # じゃんけん
    if "グー" in text or "チョキ" in text or "パー":
        result = random.choice(("グー", "チョキ", "パー"))
         # あいこ
        if result == text: 
            return "@{} {}なん！あいこなん！".format(screen_name, result)
        # 勝ちパターン
        if result == "グー" and text == "チョキ":
            return "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        if result == "チョキ" and text == "パー": 
            return "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        if result == "パー" and text == "グー": 
            return "@{} {}なん！うちの勝ちなん！".format(screen_name, result)
        # 負けパターン
        if result == "グー" and text == "パー":
            return "@{} {}なん！うちの負けなん！".format(screen_name, result)
        if result == "チョキ" and text == "グー":
            return "@{} {}なん！うちの負けなん！".format(screen_name, result)
        if result == "パー" and text == "チョキ":
            return "@{} {}なん！うちの負けなん！".format(screen_name, result)
    if text:
        if not get_tweets():
            fetch_timeline_tweets()
        sentence_1, sentence_2 = make_tweet_sentences() 
        return "@{} {}".format(screen_name, sentence_1)
    return None