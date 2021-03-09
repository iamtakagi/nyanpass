FROM python:3.9.2

RUN apt update
RUN apt install -y mecab libmecab-dev mecab-ipadic-utf8 swig
RUN git clone --depth=1 https://github.com/neologd/mecab-ipadic-neologd
RUN cd ./mecab-ipadic-neologd && ./bin/install-mecab-ipadic-neologd -y -p /var/lib/mecab/dic/mecab-ipadic-neologd
RUN rm -rf ./mecab-ipadic-neologd
RUN ln -s /var/lib/mecab/dic /usr/lib/mecab/dic

ENV MECABRC="/etc/mecabrc"

ARG SCREEN_NAME
ARG CK
ARG CS
ARG AT
ARG ATS

ENV SCREEN_NAME=$SCREEN_NAME
ENV CK=$CK
ENV CS=$CS
ENV AT=$AT
ENV ATS=$ATS

WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && \
    pipenv install --system
COPY . .

ENTRYPOINT ["python3"]
CMD ["src/main.py"]