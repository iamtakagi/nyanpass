
import datetime
from typing import Any, cast

from MakeSentence import MakeSentence
from TimelineTweets import GatherTimelineTweets
from TwitterAPI import twitter_api

import numpy as np


def Tweet():
    """ ツイートを送信する """

    # Twitter のタイムラインからツイートを取得して貯めておく
    GatherTimelineTweets()

    # 10%の確率で「にゃんぱすー」を呟く
    if np.random.randint(1,91) == 1:
        media = twitter_api.media_upload("assets/renge.gif")
        twitter_api.update_status(status = "にゃんぱすー", media_ids=[media.media_id])

    # 文章を生成
    sentence_1 = MakeSentence()
    sentence_2 = MakeSentence()

    # ツイートを送信
    tweet_result_1 = twitter_api.update_status(status=sentence_1)
    tweet_result_2 = twitter_api.update_status(status=sentence_2)
    status_link_1 = f'https://twitter.com/{tweet_result_1.user.screen_name}/status/{tweet_result_1.id}'
    status_link_2 = f'https://twitter.com/{tweet_result_1.user.screen_name}/status/{tweet_result_2.id}'
    line_break = '\n'  # f-string ではバックスラッシュが使えないので苦肉の策
    print(f'Tweet: {sentence_1.replace(line_break, " ")} ({status_link_1})')
    print(f'Tweet: {sentence_2.replace(line_break, " ")} ({status_link_2})')


# 直接実行されたときにツイートする
if __name__ == '__main__':
    Tweet()
