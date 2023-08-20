# nyanpass

## 開発

### 事前準備

```bash
$ cp .env.example .env
$ nano .env  # かんきょうへんすうを 設定する
```

### コンテナイメージのビルド

```bash
$ make build  # or docker-compose build
```

### コンテナを起動

```bash
$ make up  # or docker-compose up -d
```

### コンテナのログを確認

```bash
$ make logs  # or docker-compose logs
```

### 試しに1回だけツイート

```bash
$ make tweet  # or docker-compose run app src/Tweet.py
```

### 試しにタイムラインからツイートを収集

```bash
$ make gather-timeline  # or docker-compose run app src/TimelineTweets.py
```

## LICENSE

[MIT](License.txt)
