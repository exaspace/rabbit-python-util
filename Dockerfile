FROM python:3.11.0-alpine3.16

ENV PATH .:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

WORKDIR /work

ADD . /work/

RUN pip install -r requirements.txt
