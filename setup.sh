#!/bin/bash
# Setup script for AI Trading Bot with Robinhood Integration

echo "=================================================="
echo "🤖 AI Trading Bot - Setup Script"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your Robinhood credentials."
else
    echo ""
    echo "⚠️  .env file already exists. Skipping..."
fi

echo ""
echo "=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Robinhood credentials"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Start the API server: python api_server.py"
echo "4. Open index.html in your browser"
echo ""
echo "⚠️  IMPORTANT: Start with ENABLE_PAPER_TRADING=True for testing!"
echo ""
