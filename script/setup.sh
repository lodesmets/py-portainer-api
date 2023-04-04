#!/usr/bin/env bash
# Setups the repository.

# Stop on errors
#set -e

cd "$(dirname "$0")/.."
# Add default vscode settings if not existing
SETTINGS_FILE=./.vscode/settings.json
SETTINGS_TEMPLATE_FILE=./.vscode/settings.default.json

if [ ! -f "$SETTINGS_FILE" ]; then
    echo "Copy $SETTINGS_TEMPLATE_FILE to $SETTINGS_FILE."
    cp "$SETTINGS_TEMPLATE_FILE" "$SETTINGS_FILE"
fi

if [ ! -n "$DEVCONTAINER" ] && [ ! -n "$VIRTUAL_ENV" ];then
  python -m venv venv
  source venv/Scripts/activate
fi

read -n 1 -s -r -p "Press any key to continue"
# install git pre-commit hook
pre-commit install

# install from source
pip install -e .
