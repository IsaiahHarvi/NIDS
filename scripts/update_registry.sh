#!/usr/bin/env bash

docker compose --profile gui build
docker compose --profile gui push
