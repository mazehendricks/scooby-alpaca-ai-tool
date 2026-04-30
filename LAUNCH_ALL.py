#!/usr/bin/env python3
"""
ALPACA TRADING BOT - MASTER LAUNCHER
Launches everything with one command:
- Web server (Flask API + HTML interface)
- Portfolio monitor (real-time terminal display)
- Auto-opens browser
"""

import os
import sys
import time
import subprocess
import webbrowser
import signal
from threading import Thread
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
PORT = int(os.getenv('FLASK_PORT', 5000))
ENABLE_PAPER_TRADING = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'

# Process tracking
processes = []

def print_banner():
    """Print startup banner"""
    print("\033[1;36m" + "=" * 80)
    print("🚀 ALPACA TRADING BOT - MASTER LAUNCHER")
    print("=" * 80 + "\033[0m")
    print()
    print("\033[1;33m📊 Starting all components...\033[0m")
    print()

def print_status(component, status, color="32"):
    """Print component status"""
    print(f"\033[{color}m{'  ✓' if status == 'OK' else '  ✗'} {component}: {status}\033[0m")

def check_requirements():
    """Check if all requirements are met"""
    print("\033[1;34m🔍 Checking requirements...\033[0m")
    
    # Check .env file
    if not os.path.exists('.env'):
        print_status(".env file", "MISSING", "31")
        print("\n\033[1;31m❌ ERROR: .env file not found!\033[0m")
        print("Please copy .env.example to .env and configure your API keys")
        return False
    print_status(".env file", "OK")
    
    # Check API keys
    api_key = os.getenv('ALPACA_API_KEY')
    secret_key = os.getenv('ALPACA_SECRET_KEY')
    if not api_key or not secret_key:
        print_status("API keys", "MISSING", "31")
        print("\n\033[1;31m❌ ERROR: API keys not configured!\033[0m")
        print("Please add your Alpaca API keys to .env file")
        return False
    print_status("API keys", "OK")
    
    # Check required files
    required_files = ['index.html', 'style.css', 'script.js', 'run_trading_app.py']
    for file in required_files:
        if not os.path.exists(file):
            print_status(f"{file}", "MISSING", "31")
            return False
        print_status(f"{file}", "OK")
    
    print()
    return True

def start_web_server():
    """Start the Flask web server"""
    print("\033[1;35m🌐 Starting web server...\033[0m")
    try:
        # Start Flask server
        process = subprocess.Popen(
            [sys.executable, 'run_trading_app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        processes.append(('Web Server', process))
        
        # Wait for server to start
        time.sleep(3)
        
        if process.poll() is None:
            print_status("Web server", f"Running on http://localhost:{PORT}")
            return True
        else:
            print_status("Web server", "FAILED TO START", "31")
            return False
    except Exception as e:
        print_status("Web server", f"ERROR: {str(e)}", "31")
        return False

def start_portfolio_monitor():
    """Start the portfolio monitor in a new terminal"""
    print("\033[1;35m📊 Starting portfolio monitor...\033[0m")
    try:
        # Determine the terminal command based on OS
        if sys.platform == 'win32':
            # Windows
            cmd = ['start', 'cmd', '/k', 'python', 'portfolio_monitor.py']
            subprocess.Popen(cmd, shell=True)
        elif sys.platform == 'darwin':
            # macOS
            cmd = ['osascript', '-e', 
                   'tell app "Terminal" to do script "cd \\"' + os.getcwd() + '\\" && python3 portfolio_monitor.py"']
            subprocess.Popen(cmd)
        else:
            # Linux - try various terminal emulators
            terminals = [
                ['gnome-terminal', '--', 'python3', 'portfolio_monitor.py'],
                ['xterm', '-e', 'python3', 'portfolio_monitor.py'],
                ['konsole', '-e', 'python3', 'portfolio_monitor.py'],
                ['x-terminal-emulator', '-e', 'python3', 'portfolio_monitor.py']
            ]
            
            launched = False
            for term_cmd in terminals:
                try:
                    subprocess.Popen(term_cmd)
                    launched = True
                    break
                except FileNotFoundError:
                    continue
            
            if not launched:
                print_status("Portfolio monitor", "No terminal emulator found - run manually", "33")
                print("  \033[33mRun in separate terminal: python3 portfolio_monitor.py\033[0m")
                return True
        
        print_status("Portfolio monitor", "Launched in new terminal")
        return True
    except Exception as e:
        print_status("Portfolio monitor", f"WARNING: {str(e)}", "33")
        print("  \033[33mRun manually in separate terminal: python3 portfolio_monitor.py\033[0m")
        return True  # Don't fail the whole launch

def open_browser():
    """Open browser to the web interface"""
    print("\033[1;35m🌐 Opening browser...\033[0m")
    try:
        time.sleep(2)  # Wait for server to be ready
        url = f'http://localhost:{PORT}'
        webbrowser.open(url)
        print_status("Browser", f"Opened {url}")
        return True
    except Exception as e:
        print_status("Browser", f"Could not auto-open: {str(e)}", "33")
        print(f"  \033[33mManually open: http://localhost:{PORT}\033[0m")
        return True

def print_summary():
    """Print summary of running components"""
    print()
    print("\033[1;32m" + "=" * 80)
    print("✅ ALL COMPONENTS LAUNCHED SUCCESSFULLY!")
    print("=" * 80 + "\033[0m")
    print()
    print("\033[1;36m📋 Running Components:\033[0m")
    print(f"  🌐 Web Interface:      http://localhost:{PORT}")
    print(f"  📊 Portfolio Monitor:  Running in separate terminal")
    print(f"  💰 Trading Mode:       {'📝 PAPER TRADING' if ENABLE_PAPER_TRADING else '💰 LIVE TRADING'}")
    print()
    print("\033[1;36m🎯 Quick Actions:\033[0m")
    print(f"  • Open web interface:  http://localhost:{PORT}")
    print(f"  • Execute manual trade: python3 execute_trade.py")
    print(f"  • View logs:           tail -f trading_bot.log")
    print()
    print("\033[1;33m⚠️  To stop all components:\033[0m")
    print("  • Press Ctrl+C in this terminal")
    print("  • Close the portfolio monitor terminal")
    print()
    print("\033[1;32m🎉 Happy Trading!\033[0m")
    print()
    print("\033[90m" + "─" * 80 + "\033[0m")
    print("\033[90mPress Ctrl+C to shutdown...\033[0m")
    print()

def cleanup(signum=None, frame=None):
    """Cleanup function to stop all processes"""
    print()
    print("\033[1;33m" + "=" * 80)
    print("🛑 SHUTTING DOWN...")
    print("=" * 80 + "\033[0m")
    print()
    
    for name, process in processes:
        try:
            print(f"\033[33m  Stopping {name}...\033[0m")
            process.terminate()
            process.wait(timeout=5)
            print(f"\033[32m  ✓ {name} stopped\033[0m")
        except subprocess.TimeoutExpired:
            print(f"\033[31m  ✗ Force killing {name}...\033[0m")
            process.kill()
        except Exception as e:
            print(f"\033[31m  ✗ Error stopping {name}: {str(e)}\033[0m")
    
    print()
    print("\033[1;32m✅ Shutdown complete\033[0m")
    print("\033[1;36mThank you for using Alpaca Trading Bot!\033[0m")
    print()
    sys.exit(0)

def main():
    """Main launcher function"""
    # Register signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    # Print banner
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print()
        print("\033[1;31m❌ Requirements check failed. Please fix the issues above.\033[0m")
        print()
        sys.exit(1)
    
    print()
    
    # Start components
    if not start_web_server():
        print()
        print("\033[1;31m❌ Failed to start web server. Check the error above.\033[0m")
        print()
        cleanup()
        sys.exit(1)
    
    print()
    
    # Start portfolio monitor (non-blocking)
    start_portfolio_monitor()
    
    print()
    
    # Open browser
    open_browser()
    
    # Print summary
    print_summary()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
            # Check if web server is still running
            for name, process in processes:
                if process.poll() is not None:
                    print(f"\033[1;31m❌ {name} stopped unexpectedly!\033[0m")
                    cleanup()
                    sys.exit(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()
