FROM python:3.9-alpine

COPY requirements.txt /tmp/
RUN apk add --update --no-cache --virtual .build-deps \
        build-base \
        git \
        make \
        bash \
        curl \
        file \
        openssl \
        perl \
        sudo \
        swig \
    \
    # runtime
    && apk add --no-cache \
        libstdc++ \
    # mecab
    && mkdir -p /tmp/mecab \
    && cd /tmp/mecab \
    && git clone https://github.com/taku910/mecab . \
    && cd mecab \
    && ./configure --enable-utf8-only \
    && make \
    && make install \
    && rm -rf /tmp/mecab \
    \
    # mecab-ipadic-neologd
    && mkdir -p /tmp/mecab-ipadic-neologd \
    && cd /tmp/mecab-ipadic-neologd \
    && git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd . \
    && ./bin/install-mecab-ipadic-neologd -n -y \
    && rm -rf /tmp/mecab-ipadic-neologd \
    \
    # pip
    && cd /tmp \
    && python -m pip install --upgrade pip \
    && pip install --no-cache-dir \
        -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt \
    \
    && apk del --purge .build-deps

ENV MECABRC="/etc/mecabrc"
ENV MECAB_DICTIONARY_PATH=/usr/local/lib/mecab/dic/mecab-ipadic-neologd

WORKDIR /app
COPY . /app/

WORKDIR /app/src
CMD [ "uvicorn", "main:app", "--host", ${HOST}, "--port", ${PORT} ]