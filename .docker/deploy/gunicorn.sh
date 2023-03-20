#!/bin/bash
cd /app/api && gunicorn -k eventlet --daemon --capture-output --enable-stdio-inheritance --workers=8 --bind=unix:/run/ecoe-api.sock openECOE-API:app
