# renchon
Renge Miyauchi bot for learning words. for [twitter.com/@nyanpassnanon](https://twitter.com/nyanpassnanon)\
Randomly select a noun from the tweets in the TL and tweet it quote a line from Renchon.

[![license](https://img.shields.io/github/license/nonnon-project/renchon)](https://github.com/nonnon-project/renchon/blob/master/LICENSE)
[![issues](https://img.shields.io/github/issues/nonnon-project/renchon)](https://github.com/nonnon-project/renchon/issues)
[![pull requests](https://img.shields.io/github/issues-pr/nonnon-project/renchon)](https://github.com/nonnon-project/renchon/pulls)
[![latest](https://github.com/nonnon-project/renchon/actions/workflows/latest.yml/badge.svg)](https://github.com/nonnon-project/renchon/actions/workflows/latest.yml)

## Install
```yml
version: '3'

services:
  app:
    container_name: renchon
    image: ghcr.io/iamtakagi/renchon:latest
    volumes:
      - ./data:/app/data
    environment:
        HOST: 0.0.0.0
        PORT: 8080
        TZ: Asia/Tokyo
        SCREEN_NAME: nyanpassnanon
        TWITTER_CK: xxx
        TWITTER_CS: xxx
        TWITTER_AT: xxx
        TWITTER_ATS: xxx
        DISCORD_WEBHOOK_URL: https://discord.com/api/webhooks/xxx/xxx
    restart: unless-stopped
    networks:
      - external_network

networks:
  external_network:
    external: true
```

## Contribution
Welcome, Issues or Pull requests.

## LICENSE
iamtakagi/renchon is provided under the MIT license.
