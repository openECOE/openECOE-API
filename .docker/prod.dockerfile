FROM nginx
RUN apt-get update \
  && apt-get install -y python3-virtualenv python3-pip \
  && rm -rf /var/lib/apt/lists/*
COPY . /app/api
WORKDIR /app/api
RUN virtualenv env
RUN env/bin/pip install poetry
RUN env/bin/pip install gunicorn
RUN env/bin/pip install requests
RUN env/bin/poetry
# RUN env/bin/pip install -r requirements.txt
EXPOSE 1081
ENV ALEMBIC_UPGRADE=DO
COPY .docker/deploy/api.conf /etc/nginx/conf.d/ecoe-api.conf
COPY .docker/deploy/alembic.sh /docker-entrypoint.d/80-alembic.sh
COPY .docker/deploy/first-run.sh /docker-entrypoint.d/90-first-run.sh
COPY .docker/deploy/gunicorn.sh /docker-entrypoint.d/99-gunicorn.sh
