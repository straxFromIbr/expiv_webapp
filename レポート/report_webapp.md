# 情報工学実験IV Webアプリケーション開発

# 1.概要
- フレームワークを活用した開発演習を行うことで，Webアプリケーション開発の基礎を身につける．


# 2.開発したWebアプリケーションの概要
開発したアプリケーションは[https://tweetquizzes.herokuapp.com](https://tweetquizzes.herokuapp.com)で公開している．
またソースコードは[straxFromIbr/expiv_webapp](https://github.com/straxFromIbr/expiv_webapp)にある．
## Webアプリケーションの機能
私たちが開発したアプリケーションは，Twitterアカウントと連携し，ユーザーの過去のツイートから「単語あてクイズ」を作成するサービスを提供するものである．

## 環境
フレームワークにはPython製のDjangoを使用し，WSGIサーバにはGunicornを使用した．また，アプリケーションはheroku上にデプロイした．
使用した主なパッケージ・ライブラリなどのバージョンは次の通りである．

- Python : 3.8.10
  - Django : 3.2.4
  - gunicorn : 20.1.0
  - django-heroku : 0.3.1
  - requests-oauthlib : 1.3.0
  - mecab-python3 : 1.0.3
  - unidic-lite : 1.0.8
- Stack : heroku-20

## 分担
SAが当アプリケーションの発案と[メインページ](https://tweetquizzes.herokuapp.com)のHTMLとCSSの作成．KMはfabiconとエラーページの作成を担当した．ITは[メインページ](https://tweetquizzes.herokuapp.com)において隠す単語の位置や数を変えたりするなどの動的な要素を作成した．HGはTwitter APIからのツイート取得，ユーザ認証などバックエンドとクラウドへのデプロイを担当した．

## 