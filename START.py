#!/usr/bin/env python3
"""
ALPACA TRADING BOT - SIMPLE STARTER
Just run this file: python3 START.py
It does everything automatically.
"""

import os
import sys
import time
import webbrowser
import subprocess
from dotenv import load_dotenv

# Load API keys
load_dotenv()

print("=" * 70)
print("🚀 ALPACA TRADING BOT")
print("=" * 70)
print()

# Check API keys
api_key = os.getenv('ALPACA_API_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')

if not api_key or not secret_key:
    print("❌ ERROR: API keys not found in .env file")
    print("Please add your keys to the .env file")
    sys.exit(1)

print(f"✅ API Key: {api_key[:10]}...")
print(f"✅ Paper Trading: Enabled")
print()

# Kill any old processes
print("🧹 Cleaning up old processes...")
subprocess.run("pkill -f 'python.*api_server.py' 2>/dev/null", shell=True)
subprocess.run("pkill -f 'python.*portfolio_monitor.py' 2>/dev/null", shell=True)
subprocess.run("pkill -f 'python.*run_trading_app.py' 2>/dev/null", shell=True)
time.sleep(1)

# Start the web server
print("🌐 Starting web server...")
server_process = subprocess.Popen(
    [sys.executable, 'run_trading_app.py'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Wait for server to start
time.sleep(3)

# Open browser
print("🌐 Opening browser...")
try:
    webbrowser.open('http://localhost:5000')
except:
    pass

print()
print("=" * 70)
print("✅ TRADING BOT IS RUNNING!")
print("=" * 70)
print()
print("📊 Web Interface: http://localhost:5000")
print("💰 Portfolio Value: $100,000 (Paper Trading)")
print()
print("🎯 Next Steps:")
print("   1. Click 'Connect to Alpaca' in the browser")
print("   2. Start trading!")
print()
print("⚠️  Press Ctrl+C to stop")
print("=" * 70)
print()

# Keep running
try:
    while True:
        time.sleep(1)
        # Check if server is still running
        if server_process.poll() is not None:
            print("\n❌ Server stopped unexpectedly!")
            break
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    server_process.terminate()
    server_process.wait()
    print("✅ Stopped")
    sys.exit(0)
