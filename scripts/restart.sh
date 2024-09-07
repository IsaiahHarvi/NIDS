#!/usr/bin/env bash

# NOTE: This is for use in a production environment.

if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
else
    echo "NIDS entry already exists in /etc/hosts"
fi

echo "Cleaning Docker Environment..."
docker-compose --profile feeder --profile gui down
docker system prune --volumes -af

read -p "Do you want to clear mongo-db data? (y/n): " clear_mongo
if [[ "$clear_mongo" == "y" ]]; then
    echo "Clearing mongo-db data..."
    docker volume rm mongo-data -f
fi

echo "-------------------------------------------------------------------"
echo "Starting Services..."
docker-compose --profile feeder --profile gui up

echo "Restarted."
