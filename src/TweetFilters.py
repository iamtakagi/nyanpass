
import json
import re


def FormatTweetText(tweet: str) -> str:
    """
    ツイートの本文から URL やハッシュタグ、リツイート表記やメンションなどの余計なテキストを除去してフォーマットする

    Args:
        tweet (str): ツイートの本文

    Returns:
        str: フィルタリングしたツイートの本文
    """

    # ref: https://deecode.net/?p=846
    # ref: https://tkstock.site/2021/12/13/python-tweet-mention-url-remove-re/

    # URL を削除
    tweet = re.sub("https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", '', tweet)

    # ハッシュタグを削除
    tweet = re.sub("#[\\w]{1,}", '', tweet)

    # リツイート表記を削除
    tweet = re.sub("RT @[\\w]{1,15}:", '', tweet)

    # @ツイートの宛先を削除
    tweet = re.sub("@[\\w]{1,15}", '', tweet)

    # 改行を削除
    tweet = tweet.replace('\n', '')

    # 絵文字を削除
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    tweet = emoji_pattern.sub('', tweet)

    # 左右の空白を削除
    tweet = tweet.strip()

    return tweet


def NormalizeTweetText(tweet: str) -> str:
    """
    ツイートの本文から記号を除去する

    Args:
        text (str): ツイートの本文

    Returns:
        str: 記号を除去したツイートの本文
    """

    blacklist = '[ @\|/:%\$&?\(\)~\.=\+\-_「」（）／　：・”“]+'
    return re.sub(blacklist, '', tweet)


def FilterBannedWords(word: str) -> str:
    """
    禁止対象のワードをフィルタリングして返す

    Args:
        word (str): フィルタリング対象のテキスト

    Returns:
        str: フィルタリングしたテキスト
    """

    # 禁止対象のワードを読み込み
    with open('assets/banned_words.json', encoding='utf-8') as json_file:
        banned_words = json.load(json_file)

    # 禁止対象のワードを削除
    for w in banned_words:
        word = word.replace(w, '')
    return word
