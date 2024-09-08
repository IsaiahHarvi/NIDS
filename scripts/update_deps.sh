#!/usr/bin/env bash

# Recompile all requirements.in files for the compose services.

BASE_DIR="deploy"
for dir in "$BASE_DIR"/*/; do
    find "$dir" -maxdepth 1 -name "*.in" | while read -r infile; do
        echo "Compiling $infile..."
        pip-compile "$infile" > /dev/null 2>&1 # -v
    done
done

echo "Done!"
