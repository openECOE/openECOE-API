#!/bin/sh
# Entrada de la imagen del API. Con el comando del API (el de por defecto), antes se aplican las migraciones y se
# crea el usuario inicial, como hacía la imagen anterior. El cronómetro y el worker arrancan sin más.
# (La imagen one-for-all tiene su propio arranque y no pasa por aquí.)
set -e
case "$*" in
  *openecoe-api:app*)
    sh /app/api/.docker/deploy/alembic.sh
    sh /app/api/.docker/deploy/first-run.sh
    ;;
esac
exec "$@"
