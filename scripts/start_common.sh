#!/usr/bin/env bash

docker-compose --profile gui down

echo "-------------------------------------------------------------------"

echo "-----------------------------------------------------------------------"
echo "View GUI at http://localhost:8000"
echo -e "-----------------------------------------------------------------------\n"


echo "-----------------------------------------------------------------------"
echo "Open Terminal Interface with the 'python3 scripts/display.py'"
echo "-----------------------------------------------------------------------"

read -p "Start micro-services? (y/n): " start
if [[ "$start" == "y" ]]; then
    docker compose --profile gui up --build
fi
