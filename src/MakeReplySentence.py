
import numpy as np
import os
import random
import re

from ChoiceRandomNoun import ChoiceRandomNoun
from MakeSentence import MakeSentence
from TimelineTweets import GetTimelineTweets, GatherTimelineTweets
from TweetFilters import NormalizeTweetText


def Omikuji() -> str:
    """
    おみくじを引いて、結果を返す

    おみくじの確率:
    大吉 = 1% (0.01)
    中吉 = 9% (0.09)
    小吉 = 10% (0.1)
    吉   = 60% (0.6)
    末吉 = 10% (0.1)
    凶   = 10% (0.1)

    Returns:
        str: おみくじの結果
    """

    # おみくじの結果を生成
    choice = np.random.choice(['大吉', '中吉', '小吉', '吉', '末吉', '凶'], p=[0.01, 0.09, 0.1, 0.6, 0.1, 0.1])

    return f'アーニャ {choice}引いた！「{ChoiceRandomNoun()}」がラッキーワード！ ワクワク！'


def Janken(tweet: str) -> str:
    """
    リプライのツイートに対してじゃんけんを行い、結果を返す

    Args:
        tweet (str): リプライ元のツイート文

    Returns:
        str: じゃんけん結果
    """

    # じゃんけん結果を取得
    result = random.choice(('グー✊', 'チョキ✌', 'パー🖐'))

    # 表記をノーマライズ
    tweet = tweet.replace('ぐー', 'グー✊') \
                 .replace('ちょき', 'チョキ✌') \
                 .replace('ぱー', 'パー🖐') \
                 .replace('グー', 'グー✊') \
                 .replace('チョキ', 'チョキ✌') \
                 .replace('パー', 'パー🖐') \
                 .replace('✊', 'グー✊') \
                 .replace('👊', 'グー✊') \
                 .replace('✌', 'チョキ✌') \
                 .replace('✋', 'パー🖐') \
                 .replace('🖐', 'パー🖐')

    janken = ''

    # あいこ
    if result in tweet:
        janken = f'アーニャ {result}だした！\nアーニャとあいこ！'

    # 勝ちパターン
    if (result == 'グー✊' and 'チョキ✌' in tweet) or \
       (result == 'チョキ✌' and 'パー🖐' in tweet) or \
       (result == 'パー🖐' and 'グー✊' in tweet):
        janken = f'アーニャ {result}だした！\nアーニャのかち！ ワクワク！'

    # 負けパターン
    if (result == 'グー✊' and 'パー🖐' in tweet) or \
       (result == 'チョキ✌' and 'グー✊' in tweet) or \
       (result == 'パー🖐' and 'チョキ✌' in tweet):
        janken = f'アーニャ {result}だした！\nアーニャのまけ… しょんぼり'

    return janken


def MakeReplySentence(tweet: str) -> str | None:
    """
    リプライ用の文章を生成する

    Args:
        tweet (str): リプライ元のツイート文

    Returns:
        str | None: リプライまたは None
    """

    # ツイートから記号を削除
    tweet = NormalizeTweetText(tweet)

    # 記号を置換
    tweet = tweet.replace(',', '') \
                 .replace('&lt;', '<') \
                 .replace('&gt;', '>') \
                 .replace('&amp;', '&') \
                 .replace('?', '？') \
                 .replace('!', '！') \
                 .replace('，', '、') \
                 .replace('．', '。') \
                 .replace(f'@{os.environ["SCREEN_NAME"]}', '')

    # おみくじ
    if re.compile(r'(?:うらな(?:って|い)|占(?:って|い)|おみくじ|運勢?)').search(tweet):
        if len(GetTimelineTweets()) == 0:
            GatherTimelineTweets()
        return Omikuji()

    # じゃんけん
    if re.compile(r'(?:[✊👊✌✋🖐]|[ぐぱグパ]ー|ちょき|チョキ)').search(tweet):
        return Janken(tweet)

    # リプライのツイートがあれば
    if tweet:

        # タイムラインから集めたツイートが空なら取得
        if len(GetTimelineTweets()) == 0:
            GatherTimelineTweets()

        # 定期ツイート同様の文章を生成して返す
        return MakeSentence()

    return None
