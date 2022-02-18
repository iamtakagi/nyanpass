FROM python:3.9.6

RUN apt update
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 swig
RUN git clone --depth=1 https://github.com/neologd/mecab-ipadic-neologd
RUN cd ./mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y -p /var/lib/mecab/dic/mecab-ipadic-neologd
RUN rm -rf ./mecab-ipadic-neologd
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

ENV MECABRC="/etc/mecabrc"
ENV MECAB_DICTIONARY_PATH=/usr/local/lib/mecab/dic/mecab-ipadic-neologd

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && \
    pipenv install --system
COPY . .

WORKDIR /app/src
CMD [ "uvicorn", "main:app", "--host", ${HOST}, "--port", ${PORT} ]