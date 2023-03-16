#!/bin/bash
cd /app/api && env/bin/gunicorn --daemon --capture-output --enable-stdio-inheritance --bind=unix:/run/ecoe-api.sock openECOE-API:app
