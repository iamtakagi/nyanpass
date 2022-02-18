import random
from urllib import response
import MeCab
import numpy as np

from filters import filter_links, filter_words, normalize_text
from templates import templates

# MeCab
mecab = MeCab.Tagger(f"-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen")

def make_reply_sentence(status):
    screen_name = status.user.screen_name
    text = status.text.replace(",", "")
    text = normalize_text(text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("?", "？").replace("!", "！").replace("，", "、").replace("．", "。") + ","
    response = "@{} 何を言っているのかうちには理解できないのん。".format(screen_name)
    # 占い
    if "占って" in text or "おみくじ" in text:
        response = "@{} {}なん！".format(status.user.screen_name, random.choice(("凶", "大凶", "末吉", "吉", "小吉", "中吉", "大吉")))
    # じゃんけん
    elif "グー" in text or "チョキ" in text or "パー" in text or "ぐー" in text or "ちょき" in text or "ぱー" in text:
        result = random.choice(("グー", "チョキ", "パー"))
         # あいこ
        if result == text: 
            response = "@{} {}なん！あいこなん！".format(status.user.screen_name, result)
        # 勝ちパターン
        elif result == "グー" and text == "チョキ":
            response = "@{} {}なん！うちの勝ちなん！".format(status.user.screen_name, result)
        elif result == "チョキ" and text == "パー": 
            response = "@{} {}なん！うちの勝ちなん！".format(status.user.screen_name, result)
        elif result == "パー" and text == "グー": 
            response = "@{} {}なん！うちの勝ちなん！".format(status.user.screen_name, result)
        # 負けパターン
        elif result == "グー" and text == "パー":
            response = "@{} {}なん！うちの負けなん！".format(status.user.screen_name, result)
        elif result == "チョキ" and text == "グー":
            response = "@{} {}なん！うちの負けなん！".format(status.user.screen_name, result)
        elif result == "パー" and text == "チョキ":
            response = "@{} {}なん！うちの負けなん！".format(status.user.screen_name, result)
    else:
        # ツイート文から名詞を抜き取って台詞風に返信する。名詞がなければ返信しない。
        nouns = []
        # フィルター
        # 文章から固有名詞だけを取り出す
        for n in [line for line in mecab.parse(text).splitlines() if "固有名詞" in line.split()[-1]]:
            # 名詞を格納
            noun = n.split("\t")[0]
            # 重複チェック
            if not noun in nouns:
                nouns.append(noun)
        # ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を2つ生成する
        s = np.random.choice(templates)
        n = filter_words(np.random.choice(nouns))
        sentence = s["gokan"] + n + s["gobi"]
        response = "@{} {}".format(status.user.screen_name, sentence)
    return response
