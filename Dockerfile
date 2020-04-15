FROM python:3.8-buster
MAINTAINER S. Guliaev <semen.guliaev@gmail.com>

WORKDIR /app
COPY src /app
COPY requirements.txt ./requirements.txt
RUN apt -qqy update && apt -qqy upgrade
RUN apt install -qqy imagemagick
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 server.py
