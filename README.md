# nyanpass

## Development

```bash
$ cp .env.example .env
$ nano .env
```

```bash
$ make build  # or docker-compose build
```

```bash
$ make up  # or docker-compose up -d
```

```bash
$ make logs  # or docker-compose logs
```

```bash
$ make tweet  # or docker-compose run app src/Tweet.py
```

```bash
$ make gather-timeline  # or docker-compose run app src/TimelineTweets.py
```

## LICENSE

[MIT](License.txt)
