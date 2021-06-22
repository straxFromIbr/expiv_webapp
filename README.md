# 情報工学実験 テーマ1 Webアプリケーション
- `expiv` : Djangoアプリケーション


## 環境構築と実行の仕方
1. このリポジトリをGoogleドライブからダウンロード
2. ダウンロードしたディレクトリに移動．
3. コンテナをビルド(5分くらいかかるかも)  
	`docker build -t pytest .`
4. コンテナ起動  
	`docker run --rm -p 8000:8000 -it pytest  /bin/bash -l`
5. プログラム実行  
	`cd webapp; python manage.py runserver 0:8000`
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
- 実環境にデプロイ．herokuやPythonAnywhereなど．PyAWはなんか簡単そう．
- フロントエンドの装飾やマスク位置の指定．CSSとJSがんばれ．
- 新規ツイート取得ボタンをフォームで．Ajaxで部分的に更新が良し．
- フロントエンド側の機能としてクイズの共有とかもアリ？
