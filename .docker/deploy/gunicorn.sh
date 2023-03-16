#!/bin/bash
cd /app/api && env/bin/gunicorn --daemon --log-file /var/log/gunicorn.log --bind=unix:/run/ecoe-api.sock openECOE-API:app
