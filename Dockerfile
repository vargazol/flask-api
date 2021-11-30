FROM python:3.10-alpine

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r $CONTAINER_HOME/requirements.txt
