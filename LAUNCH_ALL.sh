#!/bin/bash
# ============================================================================
# Alpaca Trading Bot - Master Launcher (Linux/Mac)
# Run this script to launch everything at once: ./LAUNCH_ALL.sh
# ============================================================================

echo "========================================================================"
echo "   ALPACA TRADING BOT - MASTER LAUNCHER"
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
echo "Checking dependencies..."
pip3 install -q -r requirements.txt 2>/dev/null || {
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
}

echo ""
echo "Starting all components..."
echo ""

# Run the master launcher
python3 LAUNCH_ALL.py
