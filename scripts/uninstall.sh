#!/usr/bin/env bash

# NOTE: This is for use in a production environment on a Linux machine.

if grep -q "# NIDS" /etc/hosts; then
    sudo sed -i '/# NIDS/,+1d' /etc/hosts
    echo "Removed NIDS entry from /etc/hosts."
fi

docker-compose down
docker kill $(docker ps -q) > /dev/null 2>&1
docker system prune --volumes -af
docker volume rm mongo-data -f > /dev/null 2>&1

echo "Cleared Docker Environment.
