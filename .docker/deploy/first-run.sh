#!/bin/sh
# Primera vez (base de datos sin organizaciones): crea la organización y el usuario administrador, si se han pasado
# ORGANIZATION, EMAIL y PASSWORD. La contraseña no se escribe en el log.
set -e
cd /app/api
if [ -z "${ORGANIZATION:-}" ] || [ -z "${EMAIL:-}" ] || [ -z "${PASSWORD:-}" ]; then
  echo "sin ORGANIZATION, EMAIL o PASSWORD: no se crea el usuario inicial"
  exit 0
fi
if flask virgin >/dev/null; then
  flask create_orga --name "$ORGANIZATION"
  flask create_user --email "$EMAIL" --password "$PASSWORD" --name "${FIRSTNAME:-}" --surname "${SURNAME:-}" \
    --organization_name "$ORGANIZATION" --admin
fi
