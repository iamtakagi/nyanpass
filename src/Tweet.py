
import datetime
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
    line_break = '\n'  # f-string ではバックスラッシュが使えないので苦肉の策
    logging.info(f'Tweet: {sentence_1.replace(line_break, " ")} ({status_link_1})')
    logging.info(f'Tweet: {sentence_2.replace(line_break, " ")} ({status_link_2})')

    # Discord に通知
    SendDiscord(status_link_1)
    SendDiscord(status_link_2)


def OnAirNotificationTweet(hashtag: str = '#tvtokyo'):
    """ 放送告知ツイートを送信する """

    # 2022年6月28日（火）以降は実行しない
    # 第1クール終了後のため
    if datetime.datetime.now() > datetime.datetime(year=2022, month=6, day=28, hour=0, minute=0, second=0):
        return

    # 画像をアップロード
    with open('assets/onair.jpg', 'rb') as file:
        media_id = (twitter_api.media_upload(file=file, filename='onair.jpg')).media_id

    # ツイートを送信
    tweet_result = twitter_api.update_status(status=hashtag, media_ids=[media_id])
    status_link = f'https://twitter.com/{tweet_result.user.screen_name}/status/{tweet_result.id}'
    logging.info(f'ONAir Notification Tweet: {status_link}')

    # Discord に通知
    SendDiscord(status_link)


# 直接実行されたときにツイートする
if __name__ == '__main__':
    Tweet()
