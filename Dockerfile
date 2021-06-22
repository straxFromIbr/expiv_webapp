FROM python:3.8


RUN apt update
RUN apt upgrade -y
RUN apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 vim

RUN git clone https://github.com/straxFromIbr/expiv_webapp.git

RUN python -m pip install --upgrade pip
RUN cd expiv_webapp && python -m pip install -r requirements.txt


ENV MECABRC=/etc/mecabrc


ENV TW_CONSUMER_KEY="your twitter consumer key"
ENV TW_CONSUMER_KEY_SECRET="your twitter consumer key secret"
ENV SECRET_KEY='django secret key'




ENV HOME=/
WORKDIR /

