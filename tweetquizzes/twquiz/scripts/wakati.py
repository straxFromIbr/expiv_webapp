#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import collections

import MeCab


class Wakati:
    """
    入力されたテキストをMecabで形態素解析し，補助語を除外したインデックスを返す．
    """
    def __init__(self, sentence):
        """
        入力テキストをパース．
        self.parse : 処理しやすいように品詞をリストにする
        self.wakati : わかち書きの配列
        self.filter_idx : フィルターの初期化
        """
        self.parser = MeCab.Tagger()
        self.sentence = sentence
        parsed = [
            word.split("\t") for word in self.parser.parse(sentence).split("\n")[:-2]
        ]
        print(parsed)
        self.parsed = [word[:4] + [word[4].split("-")] + word[5:] for word in parsed]
        print(self.parsed)
        self.wakati = [word[0] for word in self.parsed]
        self.filter_idx = list(range(len(self.parsed)))

    def attr_filter(self, attr, lvl=0):
        """
        品詞フィルターの追加．attrが品詞，lvlが品詞の深さ
        """
        new_filter_idx = [
            idx
            for idx, word in enumerate(self.parsed)
            if word[4][min(lvl, len(word[4]) - 1)] != attr
        ]

        self.filter_idx = sorted(
            [
                k
                for k, v in collections.Counter(
                    self.filter_idx + new_filter_idx
                ).items()
                if v > 1
            ]
        )

    def apply_filter(self):
        """
        フィルターに一致する形態素のリストを返す
        """
        return [self.wakati[idx] for idx in self.filter_idx]

    def replace_random(self, nbreplace=3, replacewith="???"):
        """
        フィルターに一致する形態素からnbreplace個をreplacewithで置換する．結局フロントエンドで実装した
        """
        wakati = [word for word in self.wakati]
        replaced_idxs = []
        for idx in random.sample(self.filter_idx, min(nbreplace, len(self.filter_idx))):
            wakati[idx] = replacewith
            replaced_idxs.append(idx)
        return replaced_idxs, wakati

    def get_filter(self):
        return self.filter_idx

    def get_parsed(self):
        return self.parsed

    def get_wakati(self):
        return self.wakati

    def get_sentence(self):
        return self.sentence

    def get_removed(self):
        """
        除外された形態素を表示する．
        """
        return [
            self.wakati[idx]
            for idx in list(set(range(len(self.wakati))) - set(self.filter_idx))
        ]


def mask_text(text, nbreplace=3):
    # print(wakati.parsed)
    # print(wakati.filter_idx)
    wakati = Wakati(text)
    # level 1 filter
    wakati.attr_filter("代名詞")
    wakati.attr_filter("連体詞")
    wakati.attr_filter("助詞")
    wakati.attr_filter("助動詞")
    wakati.attr_filter("接尾辞")
    wakati.attr_filter("接頭辞")
    wakati.attr_filter("記号")
    wakati.attr_filter("補助記号")
    wakati.attr_filter("接続詞")

    # level 2 filter
    wakati.attr_filter("非自立", lvl=1)
    wakati.attr_filter("非自立可能", lvl=1)
    wakati.attr_filter("副詞可能", lvl=2)

    # print(wakati.filter_idx)
    replaced_idxs, replaced = wakati.replace_random(nbreplace=nbreplace)
    return replaced_idxs, (lambda text: text if text[-1] != " " else text[:-1])(
        "".join([(lambda w: w + " " if w.isascii() else w)(word) for word in replaced])
    )


def parse_filter(text):
    """
    フィルターを適用し，フィルターリストとわかち書きリストを返す．
    """
    wakati = Wakati(text)

    if len(wakati.wakati) <= 1:
        parse_filter_dic = {
            "filter_idxs": [],
            "wakati": wakati.wakati,
        }
        return parse_filter_dic

    # append filter
    wakati.attr_filter("代名詞")
    wakati.attr_filter("連体詞")
    wakati.attr_filter("助詞")
    wakati.attr_filter("助動詞")
    wakati.attr_filter("接尾辞")
    wakati.attr_filter("接頭辞")
    wakati.attr_filter("記号")
    wakati.attr_filter("補助記号")
    wakati.attr_filter("接続詞")
    wakati.attr_filter("非自立", lvl=1)
    wakati.attr_filter("非自立可能", lvl=1)
    wakati.attr_filter("接尾", lvl=1)
    wakati.attr_filter("副詞可能", lvl=2)
    wakati.attr_filter("サ変", lvl=4)
    # print(wakati.apply_filter())
    return {
        "filter_idxs": wakati.filter_idx,
        "wakati": wakati.wakati,
    }


if __name__ == "__main__":
    from pprint import pprint

    text = (
        "日本では、テレビやラジオ、映画などの放送、小説や漫画、新聞などの出版の分野でも、"
        + "日本語が使われることがほとんどである。国外のドラマや映画が放送される場合でも、基本"
        + "的には日本語に訳し、字幕を付けたり声を当てたりしてから放送されるなど、受け手が日本"
        + "語のみを理解することを当然の前提として作成される。原語のまま放送・出版されるものも"
        + "存在するが、それらは外国向けに発表される前提の論文、もしくは日本在住の外国人、ある"
        + "いは原語の学習者など限られた人を対象としており、大多数の日本人に向けたものではない"
        + "。語彙は、古来の大和言葉（和語）のほか、漢語（字音語）、外来語、および、それらの混"
        + "ざった混種語に分けられる。字音語（漢字の音読みに由来する語の意、一般に「漢語」と称"
        + "する）は、漢文を通して古代・中世の中国から渡来した語またはそれらから派生した語彙で"
        + "あり、現代の語彙の過半数を占めている。また、「紙（かみ）」「絵/画（ゑ）」など、もと"
        + "もと音であるが和語と認識されているものもある。さらに近代以降には西洋由来の語を"
        + "中心とする外来語が増大している（「語種」の節参照）。"
    )
    # text = "This is 天堂真矢"
    replaced_idxs, masked = mask_text(text, 50)
    # print("".join(masked))
    # print(replaced_idxs)
    dic = parse_filter(text)
    wakati = dic["wakati"]
    filter_idxs = dic["filter_idxs"]
    print(wakati)
    print(filter_idxs)
    # text = "（「語種」の節参照）"
    # wakati = Wakati(text)
    # print(wakati.parsed)
