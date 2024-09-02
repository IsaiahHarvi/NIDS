#!/usr/bin/env bash

if ! docker network inspect services >/dev/null 2>&1; then
    echo "Network 'services' not found. Creating it..."
    docker network create services
else
    echo "Network 'services' already exists."
fi
