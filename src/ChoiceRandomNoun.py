
import logging
import MeCab
import numpy as np

from TweetFilters import FilterBannedWords, FilterLinkAndReplies
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
    tweets = FilterLinkAndReplies(GetTimelineTweets())

    # フィルターを掛ける
    for tweet in tweets:
        tweet.replace('&lt;', '<') \
             .replace('&gt;', '>') \
             .replace('&amp;', '&') \
             .replace('?', '？') \
             .replace('!', '！') \
             .replace('，', '、') \
             .replace('．', '。') + ','

    # ツイートリストを出力
    logging.debug(tweets)

    # 名詞を格納するリスト
    nouns = []

    # ツイートごとに
    for tweet in tweets:
        tweet = tweet.replace(',', '')

        # 形態素出力
        parsed: str = mecab.parse(tweet)
        logging.debug(parsed)

        # 全ての文章から固有名詞だけを取り出す
        for n in [line for line in parsed.splitlines() if '固有名詞' in line.split()[-1]]:
            noun = n.split("\t")[0]
            # 重複チェック
            if not noun in nouns:
                # 名詞を格納
                nouns.append(noun)

    # 禁止対象のワードをフィルタリングしてから返す
    return FilterBannedWords(np.random.choice(nouns))
