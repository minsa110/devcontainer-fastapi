#!/bin/sh
# set -eu

echo "Starting 'redis' container..."

# Check if the "redis" container is running
if ! docker ps --filter "status=running" --format "{{.Names}}" | grep -q "redis"; then
  # If the "redis" container is not running, start it using docker-compose
  docker-compose -f ./docker-compose.yml up -d
  echo "Successfully started 'redis' container."
else
  echo "The 'redis' container is already running."
fi
