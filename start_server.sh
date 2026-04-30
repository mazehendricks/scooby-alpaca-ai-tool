#!/bin/bash
# Quick start script for the API server

echo "🚀 Starting AI Trading Bot API Server..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please run setup.sh first and configure your credentials."
    exit 1
fi

# Start the server
python api_server.py
