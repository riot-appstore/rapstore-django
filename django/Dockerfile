# Copyright (C) 2018 FU Berlin and HAW Hamburg
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y cron
ADD crontab /etc/cron.d/fetch_riot
RUN chmod 0644 /etc/cron.d/fetch_riot
RUN mkdir /code
RUN mkdir /apps
COPY . /code/
RUN git clone https://github.com/RIOT-OS/RIOT.git
WORKDIR /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
