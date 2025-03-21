#!/usr/bin/env bash

docker-compose --profile gui down

echo "-------------------------------------------------------------------"

echo "-----------------------------------------------------------------------"
echo "View GUI at http://localhost:8000"
echo -e "-----------------------------------------------------------------------\n"


echo "-----------------------------------------------------------------------"
echo "If installed, open Terminal Interface with 'uv run scripts/display.py'"
echo "-----------------------------------------------------------------------"

read -p "Start micro-services? (y/n): " start
if [[ "$start" == "y" ]]; then
    docker compose --profile gui up --build
fi
