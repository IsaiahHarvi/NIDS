#!/usr/bin/env bash

docker-compose --profile gui down

echo "-------------------------------------------------------------------"
echo "Starting Services..."

docker compose --profile gui up --build -d
echo "-----------------------------------------------------------------------"
echo "View GUI at http://localhost:8000"
echo -e "-----------------------------------------------------------------------\n"


echo "-----------------------------------------------------------------------"
echo "Open Terminal Interface with the 'python3 scripts/display.py'"
echo "-----------------------------------------------------------------------"
