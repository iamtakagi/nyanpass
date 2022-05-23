import os
from typing import Any, Dict
import tweepy
import logging
import urllib
from discordWebhook import post_discord_webhook
from makeReplySentence import make_reply_sentence
from twitterApi import api

class ReplyStream(tweepy.Stream):

    def on_status(self, status: Dict[str, Any]):
        print("[Info] Retrieved tweet: ", status.text)
        status_link = f'https://twitter.com/{status.user.screen_name}/status/{status.id}'
        post_discord_webhook(status_link, status.user.profile_image_url_https)
        reply_msg = make_reply_sentence(status)
        if reply_msg == None: pass
        if f'@{os.environ["SCREEN_NAME"]}' in reply_msg:
            pass
            print(f'This tweet contains reply to @{os.environ["SCREEN_NAME"]}, skipped.')
        else:
            reply_result = api.update_status('@{} {}'.format(status.user.screen_name, reply_msg), in_reply_to_status_id=status.id)
            reply_link = f'https://twitter.com/{os.environ["SCREEN_NAME"]}/status/{reply_result.id}'
            post_discord_webhook(reply_link)
        return True

    def on_error(self, status_code: int) -> bool:
        logging.error(f'Error Occurred. Status Code: {status_code}')
        return False