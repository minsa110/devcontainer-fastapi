#!/bin/sh
PLUGIN_HOSTNAME=$(echo "$PLUGIN_HOSTNAME" | sed 's/^"//' | sed 's/"$//')
sed -i 's|https://your-app-url.com|'$PLUGIN_HOSTNAME'|g' ./.well-known/ai-plugin.json ./.well-known/openapi.yaml ./server/main.py

exec uvicorn server.main:app --host 0.0.0.0 --port "${PORT:-${WEBSITES_PORT:-8080}}"