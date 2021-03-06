FROM python:3.7.3-alpine

ENV PATH .:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /work

ADD . /work/

RUN pip3 install -r requirements.txt
