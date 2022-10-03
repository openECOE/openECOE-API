#!/bin/bash
if [ "$ALEMBIC_UPGRADE" = "DO" ]
then
cd /app/api
export FLASK_APP=app/model/__init__.py 
./env/bin/flask db upgrade
fi;
