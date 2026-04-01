#!/bin/bash
set -e

# Esperar a que MySQL esté listo (sin conectarse a una base de datos específica)
until mysqladmin ping -h"$OPENECOE_DB_HOST" -u"$OPENECOE_DB_USER" -p"$OPENECOE_DB_PASSWORD" --silent; do
  echo "Esperando a la base de datos..."
  sleep 2
done

# Crear la base de datos si no existe
mysql -h"$OPENECOE_DB_HOST" -u"$OPENECOE_DB_USER" -p"$OPENECOE_DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $OPENECOE_DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"


echo ">>> Ejecutando migraciones Alembic..."
#flask db upgrade || true
flask db upgrade
echo "🌱 Insertando datos iniciales..."
ARCHIVE_ROUTE=/app/api/archive python /app/api/seed.py
python /app/api/seed.py

echo ">>> Ejecutando first-run..."
/docker-entrypoint.d/90-first-run.sh || true

echo ">>> Lanzando servidor Chrono en segundo plano..."
python /app/api/openecoe-chrono.py &

echo ">>> Lanzando servidor Flask..."
exec flask run --host=0.0.0.0 --port=5000