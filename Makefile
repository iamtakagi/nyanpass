
MAKEFLAGS += --no-print-directory

# Bot サービスをバックグラウンドで起動
up:
	@docker-compose up -d

# コンテナをビルドする
build:
	@docker-compose build

# 試しに単発でツイートする（デバッグ用）
tweet:
	@docker-compose run app src/Tweet.py

# 試しにタイムラインからツイートを取得する（デバッグ用）
fetch-timeline:
	@docker-compose run app src/TimelineTweets.py
