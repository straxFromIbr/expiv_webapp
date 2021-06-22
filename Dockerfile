FROM python:3.8


RUN apt update
RUN apt upgrade -y
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 vim

COPY ./tweetquizzes /tweetquizzes

RUN python -m pip install --upgrade pip
RUN cd /tweetquizzes && python -m pip install -r requirements.txt



ENV HOME=/
WORKDIR /

