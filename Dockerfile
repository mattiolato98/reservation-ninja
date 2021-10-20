# pull official base image
FROM python:3.9.7-alpine

# set work directory
WORKDIR .

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
ENV ADMIN_ENABLED 0
ENV SECURE_SSL_REDIRECT 1
ENV SESSION_COOKIE_SECURE 1
ENV CSRF_COOKIE_SECURE 1
ENV TZ Europe/Rome

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev libc-dev musl-dev libffi-dev openssl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add --no-cache tzdata

# get all the prereqs
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk \
    && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk \
    && apk add glibc-2.30-r0.apk \
    && apk add glibc-bin-2.30-r0.apk

# install Firefox
RUN apk add firefox-esr

# install vim editor
RUN apk add vim

# install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz \
    && tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin \
    && geckodriver --version

# install dependencies
COPY requirments.txt .
RUN pip install --upgrade pip \
    && pip install -r requirments.txt

# copy project
COPY . .

# set timezone info
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apk del tzdata

# collect static files and migrate
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D ninja
USER ninja

# run gunicorn
CMD gunicorn reservation_tool_base_folder.wsgi:application --bind 0.0.0.0:$PORT