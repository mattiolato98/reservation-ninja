# pull official base image
FROM python:3.9.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0
ENV ADMIN_ENABLED 0
ENV SECURE 1
ENV TZ Europe/Rome

# install psycopg2
RUN apt-get update \
    && apt-get install -y gcc python3-dev python3-pip libc-dev musl-dev libffi-dev libssl-dev \
    # postgresql postgresql-contrib?
    && apt-get install --no-install-recommends -y libpq-dev \
    # psycopg2?
    && python3 -m pip install psycopg2-binary \
    && apt-get install --no-install-recommends -y tzdata

# install Firefox
RUN apt-get install --no-install-recommends -y firefox-esr

# install vim editor
RUN apt-get install --no-install-recommends -y vim

RUN groupadd --system ninja && useradd --system ninja --gid ninja

ENV HOME=/home/ninja
ENV APP_HOME=/home/ninja/web
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# set timezone info
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get remove -y tzdata \
    && apt-get autoremove -y

# collect static files and migrate
RUN python manage.py collectstatic --noinput

RUN chown -R ninja:ninja $APP_HOME

# add and run as non-root user
USER ninja

# run gunicorn
CMD gunicorn reservation_tool_base_folder.wsgi:application --bind 0.0.0.0:$PORT
