#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import random
import re
import string


from requests_oauthlib import OAuth1Session

try:
    from .wakati import Wakati
except ImportError:
    try:
        from wakati import Wakati
    except ImportError:
        print("exits for unable to import mask tweets")
        sys.exit(1)


class MaskTweets:
    """
    ツイートを取得し，URLや返信などを除く
    """

    def __init__(self, keys):
        """
        与えられたキー(keys)をでOAuthセッションを開始する．
        """
        self.url_ptn = re.compile(r"http[\/\.\?\-:&#=_a-zA-Z0-9]*")
        self.name_ptn = re.compile(r"^@[A-Za-z0-9_]*")
        self.session = OAuth1Session(*keys)
        self.url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        self.tweets = []
        self.name = ""

    def set_name(self, name):
        self.name = name

    def lint_tweet(self, tweet):
        """
        URLと返信のパターンを除外する
        返信は除外しないことにしよう．
        記号は空白に置換
        """
        tweet = self.url_ptn.sub("", tweet)
        # for p in string.punctuation:
        #     tweet = tweet.replace(p, '　')
        return tweet

    def dl_tweet(self, nbtweets):
        """
        nbtweetsだけツイートを取得する．
        """
        if self.name == "":
            params = {
                "count": nbtweets + 1,
                "include_rts": "false",
                "exclude_replies": "true",
                "tweet_mode": "extended",
            }

        else:
            params = {
                "screen_name": self.name,
                "count": nbtweets + 1,
                "include_rts": "false",
                "exclude_replies": "true",
                "tweet_mode": "extended",
            }
        req = self.session.get(self.url, params=params)
        if req.status_code == 200:
            res = json.loads(req.text)
            self.tweets += [self.lint_tweet(line["full_text"]) for line in res]
            return True
        else:
            print(json.loads(req.text))
            return False

    # def mask_tweet(self, nbreplace=3):
    #     tweet = random.choice(self.tweets)
    #     return mask_text(tweet, nbreplace=nbreplace)

    def get_tweets(self):
        return self.tweets

    def get_rnd_wakatitweets(self):
        tweet = random.choice(self.get_tweets())
        return Wakati(tweet)


# def masktweet(name, nbtweets, nbmasks):
#     tweet = MaskTweets(name)
#     tweet.dl_tweet(nbtweets)
#     return tweet.mask_tweet(nbmasks)


def remove_huzoku(tweet):
    wakati = Wakati(tweet)
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

    return [wakati.wakati, wakati.filter_idx]


if __name__ == "__main__":
    from pprint import pprint

    try:
        from .local_settings.apikeys import (
            CONSUMER_KEY,
            CONSUMER_KEY_SECRET,
        )
    except ImportError:
        from local_settings.apikeys import (
            CONSUMER_KEY,
            CONSUMER_KEY_SECRET,
        )

    keys = (
        CONSUMER_KEY,
        CONSUMER_KEY_SECRET,
        "1221568044087951360-zJf3aopGCro7OkFEMmrqyXbO1HR1kN",
        "QXEx0GlHC5oicHBLs55dx36KAR8Cx3VNFfSOrHCnuWwfK",
    )

    tweet = MaskTweets(keys=keys)
    if tweet.dl_tweet(10):
        print(tweet.tweets)
        print(remove_huzoku(random.choice(tweet.tweets)))
