#!/bin/bash
cd /app/api
gunicorn openECOE-API:app --daemon --worker-class eventlet --capture-output --enable-stdio-inheritance --bind=127.0.0.1:5000 --reload
