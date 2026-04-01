#!/bin/bash
if [ "$ALEMBIC_UPGRADE" = "DO" ]
then
echo "🏁 Ejecutando migraciones Alembic..."
cd /app/api
flask db upgrade
fi;
