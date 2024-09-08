#!/usr/bin/env bash

# NOTE: This is for use in a production environment.

if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
fi

read -p Do you want to clean the Docker environment? \(y/n\): clean_docker
if [[ "$clean_docker" == "y" ]]; then
    echo "Cleaning Docker Environment..."
    docker-compose --profile feeder --profile gui down
    docker system prune --volumes -af
fi

read -p "Do you want to clear mongo-db data? (y/n): " clear_mongo
if [[ "$clear_mongo" == "y" ]]; then
    echo "Clearing mongo-db data..."
    docker volume rm mongo-data -f
fi

echo "-------------------------------------------------------------------"
echo "Restarting Services..."
docker-compose --profile feeder --profile gui up
