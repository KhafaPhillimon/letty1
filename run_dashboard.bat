@echo off
REM AI-Solutions Web Server Analytics Dashboard - Windows Launcher
REM This script installs dependencies and starts the dashboard

echo.
echo ============================================================
echo  AI-Solutions Web Server Analytics Dashboard
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version

echo.
echo [2/3] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/3] Generating dataset (if needed)...
if not exist "web_server_logs.csv" (
    python generate_dataset.py
)

echo.
echo ============================================================
echo  Starting Dashboard...
echo ============================================================
echo.
echo Dashboard will be available at: http://127.0.0.1:8050
echo.
echo Press Ctrl+C to stop the server
echo.

python dashboard.py

pause
