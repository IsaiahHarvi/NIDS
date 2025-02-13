#!/usr/bin/env bash

docker run -d -p 172.17.0.1:42069:5000 --name registry registry:2

docker compose --profile gui build

docker compose --profile gui push
