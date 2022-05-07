
import json
import numpy as np
from typing import Tuple

from ChoiceRandomNoun import ChoiceRandomNoun


def MakeSentences() -> Tuple[str, str]:
    """
    ランダムな名詞を選び、語幹 + 名詞 + 語尾 の形で文章を2つ生成する

    Returns:
        Tuple[str, str]: 文章
    """

    # テンプレートを読み込み
    with open('assets/templates.json', encoding='utf-8') as json_file:
        templates = json.load(json_file)

    # テンプレートからランダムにチョイス
    template_1 = np.random.choice(templates)
    template_2 = np.random.choice(templates)

    # テンプレートとランダムな名詞を組み合わせて文章を2つ生成
    sentence_1 = template_1['gokan'] + ChoiceRandomNoun() + template_1['gobi']
    sentence_2 = template_2['gokan'] + ChoiceRandomNoun() + template_2['gobi']

    # 文章を返す
    return sentence_1, sentence_2
