@echo off
REM Launch Magic Square PyQt GUI (requires .venv with PyQt6)
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt -q
)
.venv\Scripts\python -m magic_square.boundary.gui
