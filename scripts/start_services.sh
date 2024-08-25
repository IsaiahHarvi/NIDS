#!/usr/bin/env bash

echo "Stopping all running containers..."
docker kill $(docker ps -q) | true

echo "Removing all containers..."
docker system prune --volumes -af | true

echo "Starting services..."
docker compose up