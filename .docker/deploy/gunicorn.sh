#!/bin/bash
cd /app/api
gunicorn openecoe-api:app --daemon --bind=127.0.0.1:5000 --reload -c /app/api/configs/gunicorn_conf.py --capture-output --enable-stdio-inheritance
gunicorn openecoe-chrono:app -k eventlet --daemon --bind=127.0.0.1:5001 --workers 1 --reload -c /app/api/configs/gunicorn_conf.py --capture-output --enable-stdio-inheritance