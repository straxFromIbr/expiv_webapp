from django.shortcuts import render, redirect

# from django.http import HttpResponse

import random

from .pyscripts.masktweets import MaskTweets, remove_huzoku
from .pyscripts.get_oatoken import get_authenticate_endpoint_url, get_access_token

# コンシューマーキーのインポート．追跡しない
from .pyscripts.local_settings.apikeys import (
    CONSUMER_KEY,
    CONSUMER_KEY_SECRET,
)


def index(request):
    """
    # メインの処理用
    セッションが確立されてない場合は account にリダイレクト
    """
    if not "tokens" in request.session:
        return redirect("account")
    tokens = request.session["tokens"]
    tweet = MaskTweets(keys=(CONSUMER_KEY, CONSUMER_KEY_SECRET, *tokens))
    if "name" in request.GET:
        tweet.name = request.GET["name"]
    if "mute" in request.GET:
        tweet.mute = request.GET["mute"]
    if tweet.dl_tweet(500):
        wakati, filter_idx = remove_huzoku(random.choice(tweet.tweets))

        text_and_filter_list = [remove_huzoku(tw) for tw in tweet.tweets]

        context = {
            "text_and_filter_list": text_and_filter_list,
            "wakati_text": wakati,
            "filter_idx": filter_idx,
        }
        return render(request, "twquiz/index.html", context)
    else:
        return render(request, "twquiz/autherr.html", context={})


def account(request):
    """
    # ユーザー認証
    セッションをクリアし寿命設定．アプリケーション認証用エンドポイントURLを生成しリダイレクト．
    失敗した場合，自身にリダイレクト → 無限に繰り返される恐れあり．他ページに飛ばすのが良い？ ->エラーページ作った(autherr)
    """
    # request.session.clear()
    ##  セッションの寿命
    request.session.set_expiry(60)
    url = "{0}://{1}/auth".format(request.scheme, request.get_host())
    ret, endpoint_url = get_authenticate_endpoint_url(
        CONSUMER_KEY, CONSUMER_KEY_SECRET, url
    )
    if ret:
        # 取得したURL
        # https://api.twitter.com/oauth/authenticate?oauth_token=??? みたいなヤツ
        return redirect(endpoint_url)
    else:
        # 失敗した時はエラーページに．ret=FalseとなるのはたいていコールバックURLのミス
        msg = endpoint_url
        return render(request, "twquiz/autherr.html", context={"msg": msg})



def auth(request):
    """
    セッション登録
    エンドポイントURLから飛ばされるコールバックURLはここ．OAuthトークンを取得しセッションに登録する．
    """
    if "denied" in request.GET:
        return render(request, "twquiz/autherr.html", context={})

    if not "oauth_token" in request.GET or not "oauth_verifier" in request.GET:
        return redirect("account")

    oauth_token = request.GET["oauth_token"]
    oauth_verifier = request.GET["oauth_verifier"]
    ret, dic = get_access_token(
        CONSUMER_KEY,
        CONSUMER_KEY_SECRET,
        oauth_token,
        oauth_verifier,
    )
    if not ret:
        return redirect("account")

    else:
        oauth_token = dic["oauth_token"]
        oauth_token_secret = dic["oauth_token_secret"]
        tokens = (
            oauth_token,
            oauth_token_secret,
        )
        request.session["tokens"] = tokens

        return redirect("index")


# def auth(request):

#     # else:
#     return redirect("account")


# def login(request):
#     return render(request, "twquiz/login.html", context={})
