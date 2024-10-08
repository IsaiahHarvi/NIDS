#!/usr/bin/env bash

docker-compose --profile feeder --profile gui down # stop any running services, just in case

echo "-------------------------------------------------------------------"
echo "Starting Services..."

docker compose --profile feeder --profile gui up --build -d
echo "-----------------------------------------------------------------------"
echo "View GUI at http://localhost:8000"
echo -e "-----------------------------------------------------------------------\n"

# Add NIDS alias to shell config
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"

fi

if ! grep -q "alias nids=" "$SHELL_CONFIG"; then
    echo "alias nids='python3 scripts/display.py'" >> "$SHELL_CONFIG"
    echo "alias NIDS='python3 scripts/display.py'" >> "$SHELL_CONFIG"
    echo "Created NIDS entry in $SHELL_CONFIG"
    source "$SHELL_CONFIG"
fi

echo "-----------------------------------------------------------------------"
echo "Open Terminal Interface with the 'NIDS' command or 'python3 display.py'"
echo "-----------------------------------------------------------------------"
