
import json
import re
from typing import List


def FilterLinkAndReplies(tweets: List[str]) -> List[str]:
    """
    ツイートのリストからリンクが含まれているもの、リプライのものを除外して返す

    Args:
        tweets (_type_): ツイートのリスト

    Returns:
        _type_: _description_
    """

    data = []
    for tweet in tweets:

        # リンクまたはリプライがツイートに含まれているツイートを除外
        if re.compile(r"https?://").search(tweet) or re.compile(r"@\w+").search(tweet):
            continue

        # それ以外を残す
        data.append(tweet)

    return data


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
