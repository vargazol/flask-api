FROM python:3.9.7-slim-buster

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip3 install -r $CONTAINER_HOME/requirements.txt