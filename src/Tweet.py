
import logging

from DiscordWebhook import SendDiscord
from MakeSentence import MakeSentence
from TimelineTweets import GatherTimelineTweets
from TwitterAPI import twitter_api


def Tweet():
    """ ツイートを送信する """

    # Twitter のタイムラインからツイートを取得して貯めておく
    GatherTimelineTweets()

    # 文章を生成
    sentence_1 = MakeSentence()
    sentence_2 = MakeSentence()

    # ツイートを送信
    tweet_result_1 = twitter_api.update_status(status=sentence_1)
    tweet_result_2 = twitter_api.update_status(status=sentence_2)
    status_link_1 = f'https://twitter.com/{tweet_result_1.user.screen_name}/status/{tweet_result_1.id}'
    status_link_2 = f'https://twitter.com/{tweet_result_1.user.screen_name}/status/{tweet_result_2.id}'
    logging.info(f'Tweet: {sentence_1} ({status_link_1})')
    logging.info(f'Tweet: {sentence_2} ({status_link_2})')

    # Discord に通知
    SendDiscord(status_link_1)
    SendDiscord(status_link_2)


# 直接実行されたときにツイートする
if __name__ == '__main__':
    Tweet()
