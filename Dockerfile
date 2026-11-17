# openECOE API: Python 3.15 sobre Debian 13 (trixie), sin root.
#
# Procesos (cada uno con su comando; la imagen one-for-all los lanza juntos con nginx delante):
#   API         gunicorn -c configs/gunicorn_conf.py openecoe-api:app              (por defecto, 0.0.0.0:5000)
#   cronómetro  gunicorn -c configs/gunicorn_conf.py -w 1 --threads 100 openecoe-chrono:app   (un solo proceso)
#   trabajos    flask rq worker
# Con el comando del API, la entrada (.docker/deploy/entrypoint.sh) aplica antes las migraciones y crea el usuario
# inicial (alembic.sh y first-run.sh).

ARG PYTHON_IMAGE=python:3.15-slim-trixie

FROM ${PYTHON_IMAGE} AS build
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1 PIP_ROOT_USER_ACTION=ignore
RUN pip install poetry==2.5.1 poetry-plugin-export==1.10.1
WORKDIR /src
COPY pyproject.toml poetry.lock ./
# Dependencias exactas del lock, con sus hashes.
RUN poetry export --only main --format requirements.txt --output requirements.txt \
 && python -m venv /opt/venv \
 && /opt/venv/bin/pip install --require-hashes --no-deps -r requirements.txt \
 && /opt/venv/bin/pip uninstall -y pip

FROM ${PYTHON_IMAGE} AS prod
ARG GIT_COMMIT="-"
# Librerías de WeasyPrint (informes PDF) y fuentes; sin binarios setuid/setgid.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 \
      fonts-dejavu-core fonts-liberation2 \
 && rm -rf /var/lib/apt/lists/* \
 && find / -xdev -perm /6000 -type f -exec chmod a-s {} + \
 && groupadd --system --gid 48 openecoe \
 && useradd --system --uid 48 --gid 48 --home-dir /nonexistent --no-create-home --shell /usr/sbin/nologin openecoe

COPY --from=build /opt/venv /opt/venv
# Código de root y sin escritura para el usuario de la aplicación.
COPY . /app/api
WORKDIR /app/api
RUN python -m compileall -q -j 0 /app/api /opt/venv \
 && rm -rf /app/api/archive \
 && PY="$(python -c 'import platform; print(platform.python_version())')" \
 && OS="$(grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2 | tr -d '"')" \
 && printf '\nopenecoe-api builded %s [%s] -> %s -> python-%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$GIT_COMMIT" "$OS" "$PY" >> /etc/os-release

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=openecoe-api.py \
    ALEMBIC_UPGRADE=DO \
    LOG_TO_STDOUT=True \
    OPENECOE_ARCHIVE_DIR=/tmp/openecoe-archive

USER 48:48
EXPOSE 5000
ENTRYPOINT ["/app/api/.docker/deploy/entrypoint.sh"]
CMD ["gunicorn", "-c", "configs/gunicorn_conf.py", "openecoe-api:app"]
