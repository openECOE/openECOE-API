FROM python:3.8-slim-buster as base

# set work directory
WORKDIR /app/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml /app/pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# copy project
COPY . /app/api

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

FROM base as prod

COPY .docker/deploy/gunicorn.sh /docker-entrypoint.d/99-gunicorn.sh

