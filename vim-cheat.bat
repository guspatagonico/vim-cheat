@echo off
REM VIM Cheat Sheet — Launch script (Windows)
cd /d "%~dp0"
if not exist .venv (
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt > nul
)
.venv\Scripts\python run.py
