#!/bin/bash
cd /app/api && gunicorn --daemon --capture-output --enable-stdio-inheritance --bind=unix:/run/ecoe-api.sock openECOE-API:app
