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
        status_link = 'https://twitter.com/{}/status/{}'.format(status.user.screen_name, status.id)
        post_discord_webhook(status_link)
        reply_msg = make_reply_sentence(status)
        if reply_msg == None: pass
        if "@nyanpassnanon" in reply_msg:
            pass
            print("This tweet contains reply to @nyanpassnanon, skipped.")
        else:
            reply_result = api.update_status('@{} {}'.format(status.user.screen_name, reply_msg), in_reply_to_status_id=status.id)
            reply_link = 'https://twitter.com/nyanpassnanon/status/{}'.format(reply_result.id)
            post_discord_webhook(reply_link)
        return True

    def on_error(self, status_code: int) -> bool:
        logging.error(f'Error Occurred. Status Code: {status_code}')
        return False