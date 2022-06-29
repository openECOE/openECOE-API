#!/bin/bash
cd /app/api && env/bin/gunicorn --daemon --bind=unix:/run/ecoe-api.sock openECOE-API:app
