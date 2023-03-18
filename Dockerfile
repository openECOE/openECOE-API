FROM nginx as base
RUN apt-get update \
  && apt-get install -y python3-virtualenv python3-pip \
  && rm -rf /var/lib/apt/lists/*
  
# set work directory
WORKDIR /app/api

# set environment variables
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV FLASK_APP=openECOE-API.py

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry

# install dependencies with Poetry
COPY pyproject.toml /app/pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install

ENV ALEMBIC_UPGRADE=DO
COPY .docker/deploy/alembic.sh /docker-entrypoint.d/80-alembic.sh
COPY .docker/deploy/first-run.sh /docker-entrypoint.d/90-first-run.sh

FROM base as debug
# Debug image reusing the base
# Install dev dependencies for debugging
RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

ENV FLASK_ENV = development
ENV FLASK_DEBUG = 1

COPY .docker/deploy/debug.sh /docker-entrypoint.d/99-debug.sh

FROM base as prod

# Production image
RUN pip install gunicorn

# Nginx config
COPY .docker/deploy/api.conf /etc/nginx/conf.d/ecoe-api.conf
EXPOSE 1081

ENV FLASK_ENV = production
ENV FLASK_DEBUG = 0

# copy project
COPY . /app/api
COPY .docker/deploy/gunicorn.sh /docker-entrypoint.d/99-gunicorn.sh

