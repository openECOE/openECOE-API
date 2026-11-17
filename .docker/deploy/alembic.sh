#!/bin/sh
# Migraciones de la base de datos (salvo ALEMBIC_UPGRADE distinto de DO).
set -e
if [ "${ALEMBIC_UPGRADE:-DO}" = "DO" ]
then
cd /app/api
flask db upgrade
fi
