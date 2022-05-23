
import json
import numpy as np

from ChoiceRandomNoun import ChoiceRandomNoun
from TweetFilters import NormalizeTweetText


# テンプレートを読み込み
with open('assets/templates.json', encoding='utf-8') as json_file:
    templates = json.load(json_file)


def MakeSentence() -> str:
    """
    ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を生成する

    Returns:
        str: 文章
    """

    # テンプレートからランダムにチョイス
    template = np.random.choice(templates)

    # ランダムな名詞を取得
    noun = ChoiceRandomNoun()

    # 名詞に記号しか含まれていなかったら再取得
    if NormalizeTweetText(noun) == '':
        noun = ChoiceRandomNoun()

    # 名詞に数字しか含まれていなかったら再取得
    if noun.isdecimal() is True:
        noun = ChoiceRandomNoun()

    # テンプレートとランダムな名詞を組み合わせて文章を生成
    sentence = template['gokan'] + noun + template['gobi']

    # 文章を返す
    return sentence
