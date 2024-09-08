#!/usr/bin/env bash

# NOTE: This is for use in a production environment on a Linux machine.

if grep -q "# NIDS" /etc/hosts; then
    sudo sed -i '/# NIDS/,+1d' /etc/hosts
    echo "NIDS entry removed from /etc/hosts"
fi

docker-compose --profile feeder --profile gui down
docker kill $(docker ps -q) > /dev/null 2>&1 | true
docker system prune --volumes -af | true
docker volume rm mongo-data -f | true

echo "Cleared Docker Environment and Removed NIDS Hosts Entry."
