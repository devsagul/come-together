FROM python:3.8-alpine
MAINTAINER S. Guliaev <semen.guliaev@gmail.com>

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add poppler poppler-utils imagemagick
WORKDIR /app
COPY src /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
ENTRYPOINT python3 server.py
