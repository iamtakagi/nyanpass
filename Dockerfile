FROM python:3.9.6

RUN apt update
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 swig
RUN git clone --depth=1 https://github.com/neologd/mecab-ipadic-neologd
RUN cd ./mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y -p /var/lib/mecab/dic/mecab-ipadic-neologd
RUN rm -rf ./mecab-ipadic-neologd
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

ENV MECABRC="/etc/mecabrc"

ARG HOST
ARG PORT
ARG TZ
ARG SCREEN_NAME
ARG TWITTER_CK
ARG TWITTER_CS
ARG TWITTER_AT
ARG TWITTER_ATS

ENV HOST=${HOST}
ENV PORT=${PORT}
ENV TZ=${TZ}
ENV SCREEN_NAME=${SCREEN_NAME}
ENV TWITTER_CK=${TWITTER_CK}
ENV TWITTER_CS=${TWITTER_CS}
ENV TWITTER_AT=${TWITTER_AT}
ENV TWITTER_ATS=${TWITTER_ATS}

COPY src/exportTweets.py /app/
RUN python exportTweets.py

COPY . /app/

# Add script to crontab
RUN echo '*/15 * * * * cd /app; python tweet.py' > /var/spool/cron/crontabs/root

# Run flask
CMD ["python", "src/main.py"]

# Run crond
ENTRYPOINT ["crond", "-f"]