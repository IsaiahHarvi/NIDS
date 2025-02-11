#!/usr/bin/env bash

if grep -q "# NIDS" /etc/hosts; then
    sudo sed -i '/# NIDS/,+1d' /etc/hosts
    echo "Removed NIDS entry from /etc/hosts."
fi

nids_containers=$(docker ps -aq --filter "name=nids-")
if [[ -n "$nids_containers" ]]; then
    echo "Stopping and removing NIDS containers..."
    docker stop $nids_containers > /dev/null 2>&1
    docker rm $nids_containers > /dev/null 2>&1
else
    echo "No NIDS containers found."
fi

docker-compose --profile gui down
docker system prune --volumes -af
docker volume rm mongo-data -f > /dev/null 2>&1

echo "Cleared Docker Environment."
