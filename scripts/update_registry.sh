#!/usr/bin/env bash

# curl -X GET http://172.17.0.1:42069/v2/_catalog

docker compose --profile gui build
docker compose --profile gui push
