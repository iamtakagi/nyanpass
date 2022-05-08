
import json
import numpy as np
from typing import Tuple

from ChoiceRandomNoun import ChoiceRandomNoun


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

    # テンプレートとランダムな名詞を組み合わせて文章を生成
    sentence = template['gokan'] + ChoiceRandomNoun() + template['gobi']

    # 文章を返す
    return sentence
