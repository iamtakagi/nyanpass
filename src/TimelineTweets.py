
import json
import os

from TweetFilters import FormatTweetText
from TwitterAPI import twitter_api


# タイムラインのツイートを保存しておく JSON
dest_file = 'data/timeline_tweets.json'


def GatherTimelineTweets():
    """ Twitter のタイムラインからツイートを収集し、JSON に保存する """

    # 書き込みモード (w) で開く
    # 開いた時点で既存のファイルの内容はクリアされる
    with open(dest_file, mode='w', encoding='utf-8') as file:

        # タイムラインからツイートを収集
        # tweet_mode='extended' を指定しないと一部のツイートが140文字ちょうどで切り詰められる
        # ref: https://docs.tweepy.org/en/stable/extended_tweets.html
        tweets = []
        for tweet in twitter_api.home_timeline(count=100, tweet_mode='extended'):

            # スクリーンネームが Bot と同じツイートを除外
            if tweet.user.screen_name == os.environ['SCREEN_NAME']:
                continue

            # # リツイートされたツイートを除外
            # if tweet.retweeted is True or 'RT @' in tweet.full_text:
            #     continue

            # ツイート本文のみをフィルタリング
            tweet_text = FormatTweetText(tweet.full_text)
            if tweet_text == '':
                continue

            tweets.append(tweet_text)

        # ensure_ascii を False にして JSON を読みやすく
        file.write(json.dumps(tweets, ensure_ascii=False, indent=4))


def GetTimelineTweets() -> list[str]:
    """
    保存したタイムラインのツイートを取得する

    Returns:
        list[str]: ツイート文のリスト
    """

    # ツイートが保存されていない場合
    if not os.path.isfile(dest_file):
        return []

    # JSON を読み込んでそのまま返す
    with open(dest_file, encoding='utf-8') as file:
        return json.load(file)


# 直接実行されたときにタイムラインからツイートを取得する（ツイートはしない）
if __name__ == '__main__':
    GatherTimelineTweets()
