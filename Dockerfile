FROM python:3.8

RUN apt update
RUN apt upgrade -y
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 vim


RUN python -m pip install --upgrade pip
RUN python -m pip install mecab-python3

ENV HOME=/
ENV MECABRC=/etc/mecabrc


WORKDIR /

