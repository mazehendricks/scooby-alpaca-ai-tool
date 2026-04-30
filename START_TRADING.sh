#!/bin/bash
# ============================================================================
# Alpaca Trading Bot - Linux/Mac Launcher
# Run this script to start the trading application: ./START_TRADING.sh
# ============================================================================

echo "========================================================================"
echo "   ALPACA TRADING BOT - STARTING..."
echo "========================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys"
    exit 1
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Run the application
echo "Starting trading application..."
echo ""
python3 run_trading_app.py
