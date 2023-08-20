FROM python:3.11-slim

ENV TZ=Asia/Tokyo

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y curl file git make mecab libmecab-dev mecab-ipadic-utf8 swig xz-utils
RUN git clone --depth=1 https://github.com/neologd/mecab-ipadic-neologd
RUN cd ./mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y -p /var/lib/mecab/dic/mecab-ipadic-neologd
RUN rm -rf ./mecab-ipadic-neologd
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

ENV MECABRC="/etc/mecabrc"
ENV MECAB_DICTIONARY_PATH=/usr/local/lib/mecab/dic/mecab-ipadic-neologd

WORKDIR /app

COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/
ENV PIPENV_VENV_IN_PROJECT=true
RUN pip install pipenv && pipenv sync

COPY . /app/

ENTRYPOINT ["pipenv", "run", "python"]
CMD ["src/main.py"]
