#!/bin/sh
PLUGIN_HOSTNAME=$(echo "$PLUGIN_HOSTNAME" | sed 's/^"//' | sed 's/"$//')
sed -i 's|https://your-app-url.com|'$PLUGIN_HOSTNAME'|g' ./ai-plugin.json ./openapi.yaml ./main.py

exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-${WEBSITES_PORT:-8080}}"