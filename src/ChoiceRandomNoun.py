
import logging
import MeCab
import numpy as np

from TweetFilters import FilterBannedWords
from TimelineTweets import GetTimelineTweets


def ChoiceRandomNoun() -> str:
    """
    TLのツイートからランダムに名詞を取得する

    Returns:
        str: ランダムに取得した名詞
    """

    # MeCab を初期化
    mecab = MeCab.Tagger('-d /usr/lib/mecab/dic/mecab-ipadic-neologd -Ochasen')

    # ツイートを取得
    tweets = GetTimelineTweets()

    # フィルターを掛ける
    for tweet in tweets:
        tweet.replace('&lt;', '<') \
             .replace('&gt;', '>') \
             .replace('&amp;', '&') \
             .replace('?', '？') \
             .replace('!', '！') \
             .replace('，', '、') \
             .replace('．', '。') + ','

    # 名詞を格納するリスト
    nouns = []

    # ツイートごとに
    for tweet in tweets:
        tweet = tweet.replace(',', '')

        # 形態素出力
        parsed: str = mecab.parse(tweet)

        try:

            # 全ての文章から固有名詞だけを取り出す
            for n in [line for line in parsed.splitlines() if '固有名詞' in line.split()[-1]]:
                noun = n.split("\t")[0]
                # 重複チェック
                if not noun in nouns:
                    # 名詞を格納
                    nouns.append(noun)

        # 何らかの要因で MeCab でうまく解析できていないので、エラーログを表示してスキップ
        except IndexError:
            logging.error('Error: MeCab parse failed.')
            logging.error('Parsed string:')
            logging.error(parsed.splitlines())

    # ランダムに名詞を取得
    # 同時に禁止対象のワードをフィルタリングする
    noun = FilterBannedWords(np.random.choice(nouns))

    # 取得した名詞が1文字だけだった場合、大抵意味が通らないのでもう一度取得し直す
    while len(noun) == 1:
        noun = FilterBannedWords(np.random.choice(nouns))

    return noun
