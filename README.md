[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# 情報工学実験 テーマ1 Webアプリケーション
- `tweetquizzes` : Djangoアプリケーションのルートディレクトリ


## 環境構築と実行の仕方
1. このリポジトリをクローン
4. ダウンロードしたディレクトリに移動．
5. 事前に共有したシークレットキーをファイルに書き込む
6. コンテナをビルド(5分くらいかかるかも)  
	`$ docker build -t twquizcont .`
4. コンテナ起動  
	`$ docker run --rm -p 8000:8000 -it twquizcont /bin/bash -l`
5. 開発サーバー起動
	``` sh
	$ cd tweetquizzes
	$ python manage.py migrate
	$ python mange.py runserver 0:8000
	```
6. Webブラウザで[http://localhost:8000](http://localhost:8000)にアクセス．



## ログインの流れ

- セッション未確立のユーザー
	1. ルート(`/`)にアクセス．セッションが空なので`/account`にリダイレクト．
	2. `/account`で，エンドポイントURLを取得し，Twitterのアプリケーション認証画面にリダイレクト
	3. `/auth`にコールバック．OAuthトークンシークレットを取得．
セッションにトークンが登録される．
		ルート(`/`)にリダイレクト．
	4. セッションに登録されたトークンでツイート取得．

- セッション確立済みのユーザ
	1. ルート(`/`)にアクセス．登録されたトークンでツイート取得．

- セッションをリフレッシュ
	1. ルート(`/`)にアクセス．リンクを踏む→`/account`にリダイレクト．
	2. あとは同じ．


# 今後のタスク
- 実環境にデプロイ．herokuやPythonAnywhereなど．PyAWはなんか簡単そう．←herokuにデプロイ済み
- フロントエンドの装飾やマスク位置の指定．CSSとJSがんばれ
- 新規ツイート取得ボタンをフォームで．Ajaxで部分的に更新が良し．←事前に複数のツイートを渡すことで解決
- フロントエンド側の機能としてクイズの共有とかもアリ？ ←検討中

