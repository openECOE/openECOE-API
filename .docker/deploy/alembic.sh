#!/bin/bash
if [ "$ALEMBIC_UPGRADE" = "DO" ]
then
cd /app/api
flask db upgrade
fi;
