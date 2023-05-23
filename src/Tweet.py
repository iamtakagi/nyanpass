
import datetime
from typing import Any, cast

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
    print(f'Tweet: {sentence_1.replace(line_break, " ")} ({status_link_1})')
    print(f'Tweet: {sentence_2.replace(line_break, " ")} ({status_link_2})')

    # Discord に通知
    SendDiscord(status_link_1)
    SendDiscord(status_link_2)


def OnAirNotificationTweet(hashtag: str = '#tvtokyo'):
    """ 放送告知ツイートを送信する """

    # 2022年12月27日（火）以降は実行しない
    # 第2クール終了後のため
    if datetime.datetime.now() > datetime.datetime(year=2022, month=12, day=27, hour=0, minute=0, second=0):
        return

    # 画像をアップロード
    with open('assets/onair.jpg', 'rb') as file:
        media_id = cast(Any, twitter_api.media_upload(file=file, filename='onair.jpg')).media_id

    # ツイートを送信
    tweet_result = twitter_api.update_status(status=hashtag, media_ids=[media_id])
    status_link = f'https://twitter.com/{tweet_result.user.screen_name}/status/{tweet_result.id}'
    print(f'ONAir Notification Tweet: {status_link}')

    # Discord に通知
    SendDiscord(status_link)


# 直接実行されたときにツイートする
if __name__ == '__main__':
    Tweet()
