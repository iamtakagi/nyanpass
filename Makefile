
MAKEFLAGS += --no-print-directory

# Bot サービスをバックグラウンドで起動
up:
	@docker-compose up -d

# コンテナをビルドする
build:
	@docker-compose build

# コンテナのログを見る
logs:
	@docker-compose logs

# 試しに単発でツイートする（デバッグ用）
tweet:
	@docker-compose run app src/Tweet.py

# 試しにタイムラインからツイートを収集する（デバッグ用）
gather-timeline:
	@docker-compose run app src/TimelineTweets.py
