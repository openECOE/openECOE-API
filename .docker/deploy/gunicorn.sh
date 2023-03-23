#!/bin/bash
cd /app/api
gunicorn openecoe-chrono:app -k eventlet --daemon  --workers 1 --bind=127.0.0.1:5000 --reload -c /app/api/configs/gunicorn_conf.py --capture-output --enable-stdio-inheritance
gunicorn openecoe-api:app --daemon --bind=unix:/run/ecoe-api.sock --reload -c /app/api/configs/gunicorn_conf.py --capture-output --enable-stdio-inheritance
