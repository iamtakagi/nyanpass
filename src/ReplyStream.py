
import logging
import os
import tweepy
from typing import Any, Dict

from MakeReplySentence import MakeReplySentence
from TwitterAPI import twitter_api


class ReplyStream(tweepy.Stream):

    def on_status(self, status: Dict[str, Any]):
        """
        自分のツイートに反応があったときのイベント

        Args:
            status (Dict[str, Any]): ツイートオブジェクト
        """

        # リプライでなければ除外
        if status.in_reply_to_user_id is None:
            return

        # リプライ元のツイートの投稿者が自アカウントのスクリーンネームだったら除外
        if status.user.screen_name == os.environ['SCREEN_NAME']:
            logging.info(f'This tweet contains reply to @{os.environ["SCREEN_NAME"]}, skipped.')
            return

        # extended_tweet があればそっちから取得
        if hasattr(status, 'extended_tweet'):
            tweet = status.extended_tweet['full_text']
        else:
            tweet = status.text
        logging.info(f'[Info] Retrieved tweet: {tweet}')

        # リプライ用の文章を生成
        reply_sentence = MakeReplySentence(tweet)

        # リプライ用の文章が生成されていない
        if reply_sentence == None:
            return

        # リプライを実行
        tweet_result = twitter_api.update_status(f'@{status.user.screen_name} {reply_sentence}', in_reply_to_status_id=status.id)
        status_link = f'https://twitter.com/{tweet_result.user.screen_name}/status/{tweet_result.id}'
        logging.info(f'Reply: {reply_sentence} ({status_link})')


    def on_error(self, status_code: int) -> bool:
        """
        エラーが発生したときのイベント

        Args:
            status_code (int): Twitter のエラーコード

        Returns:
            bool: 常に False を返す
        """

        if status_code == 420:
            logging.error('[Error] 420')
            return False
        else:
            logging.error(f'[Error] {status_code}')
            return False
