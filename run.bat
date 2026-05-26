@echo off
REM Start NameDecoder met de juiste venv-Python (3.13), niet de globale 3.14.
cd /d "%~dp0"
".venv\Scripts\python.exe" main.py
