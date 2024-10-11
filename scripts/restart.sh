#!/usr/bin/env bash

if ! grep -q "# NIDS" /etc/hosts; then
    echo -e "\n# NIDS\n127.0.0.1 mongo" | sudo tee -a /etc/hosts
    echo "NIDS entry added to /etc/hosts"
fi

docker-compose --profile feeder --profile gui down

read -p "Do you want to clean the Docker environment? (y/n): " clean_docker
if [[ "$clean_docker" == "y" ]]; then
    echo "Cleaning Docker Environment..."
    docker system prune --volumes -af
fi

read -p "Do you want to clear mongo-db data? (y/n): " clear_mongo
if [[ "$clear_mongo" == "y" ]]; then
    echo "Clearing mongo-db data..."
    docker volume rm mongo-data -f
fi

bash scripts/start_common.sh
