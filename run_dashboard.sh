#!/bin/bash
# AI-Solutions Web Server Analytics Dashboard - Unix/Linux/Mac Launcher
# This script installs dependencies and starts the dashboard

echo ""
echo "============================================================"
echo "  AI-Solutions Web Server Analytics Dashboard"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version

echo ""
echo "[2/3] Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[3/3] Generating dataset (if needed)..."
if [ ! -f "web_server_logs.csv" ]; then
    python3 generate_dataset.py
fi

echo ""
echo "============================================================"
echo "  Starting Dashboard..."
echo "============================================================"
echo ""
echo "Dashboard will be available at: http://127.0.0.1:8050"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 dashboard.py
