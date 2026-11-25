#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ "$1" = "--version" ] || [ "$1" = "-V" ]; then
    exec .venv/bin/python colab_leecher/_version.py
fi
exec .venv/bin/python -m colab_leecher
