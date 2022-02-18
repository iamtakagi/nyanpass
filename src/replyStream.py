from tweepy import Stream, StreamListener
from makeReplySentence import make_reply_sentence
from twitterApi import api

# Twitter streaming
class ReplyStreamListener(StreamListener):

    def on_status(self, status):
        print("[Info] Retrieved tweet: ", status.text)
        reply_msg = make_reply_sentence(status)
        if reply_msg == None: pass
        if "@nyanpassnanon" in reply_msg:
            pass
            print("This tweet contains reply to @nyanpassnanon, skipped.")
        else:
            api.update_status(reply_msg, in_reply_to_status_id=status.id)
            print("Sent tweet: {}".format(reply_msg))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print('[Error] 420')
            return False
        else:
            print(f'[Error] {status_code}')
            return False

class ReplyStream():
    def __init__(self, auth, listener):
        self.stream = Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.filter(track=["@nyanpassnanon"], languages=["ja"])