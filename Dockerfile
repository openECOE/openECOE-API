#FROM python:3.8.16 as build
FROM nginx as base
RUN apt-get update && \
    apt-get install -y python3-pip python3-venv  && \
    python3 -m pip install --upgrade pip && \
    pip3 install wheel

RUN pip install poetry

WORKDIR /app/api

# install dependencies with Poetry
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
RUN poetry export --format=requirements.txt --output=requirements.txt --with chrono --with api --without-hashes

# set work directory
COPY . /app/api

# set environment variables
RUN virtualenv /app/api/env
ENV PATH=/app/api/env/bin:$PATH

RUN /app/api/env/bin/pip install --no-cache -r requirements.txt

ENV FLASK_APP=openecoe-api.py

ENV ALEMBIC_UPGRADE=DO

FROM base as prod
# Nginx config
COPY .docker/deploy/api.conf /etc/nginx/conf.d/default.conf
ENV FLASK_ENV = production
ENV FLASK_DEBUG = 0

# Pre Start Nginx Scripts
COPY .docker/deploy/alembic.sh /docker-entrypoint.d/80-alembic.sh
COPY .docker/deploy/first-run.sh /docker-entrypoint.d/90-first-run.sh
COPY .docker/deploy/gunicorn.sh /docker-entrypoint.d/99-gunicorn.sh

EXPOSE 8081