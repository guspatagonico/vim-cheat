#!/usr/bin/env bash
# VIM Cheat Sheet — Launch script (Linux/macOS)
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt > /dev/null
fi
.venv/bin/python run.py
