#!/bin/bash
cd /app/api && env/bin/gunicorn --daemon --access-logfile /var/log/gunicorn/access.log --error-logfile /var/log/gunicorn/error.log --capture-output --bind=unix:/run/ecoe-api.sock openECOE-API:app
