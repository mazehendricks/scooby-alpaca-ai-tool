# 🚀 ONE-CLICK LAUNCHER - Complete Guide

## 🎯 Launch Everything with One Command

The master launcher starts **ALL components** automatically:
- ✅ Web server (Flask API)
- ✅ HTML trading interface
- ✅ Portfolio monitor (real-time terminal)
- ✅ Auto-opens browser

## 🖱️ How to Use

### Windows (Double-Click)
```
Double-click: LAUNCH_ALL.bat
```

### Linux/Mac (Terminal)
```bash
./LAUNCH_ALL.sh
```

### Or Direct Python
```bash
python3 LAUNCH_ALL.py
```

## 📋 What Happens When You Launch

### 1. **Requirements Check** ✓
- Verifies `.env` file exists
- Checks API keys are configured
- Validates required files (HTML, CSS, JS)

### 2. **Web Server Starts** 🌐
- Flask API server launches on port 5000
- Serves HTML trading interface
- Provides REST API endpoints

### 3. **Portfolio Monitor Opens** 📊
- Opens in a **new terminal window**
- Shows real-time portfolio updates
- Updates every 5 seconds

### 4. **Browser Opens** 🌐
- Automatically opens http://localhost:5000
- Shows trading interface
- Ready to connect and trade

## 🎨 What You'll See

### Main Terminal (Launcher)
```
================================================================================
🚀 ALPACA TRADING BOT - MASTER LAUNCHER
================================================================================

🔍 Checking requirements...
  ✓ .env file: OK
  ✓ API keys: OK
  ✓ index.html: OK
  ✓ style.css: OK
  ✓ script.js: OK
  ✓ run_trading_app.py: OK

🌐 Starting web server...
  ✓ Web server: Running on http://localhost:5000

📊 Starting portfolio monitor...
  ✓ Portfolio monitor: Launched in new terminal

🌐 Opening browser...
  ✓ Browser: Opened http://localhost:5000

================================================================================
✅ ALL COMPONENTS LAUNCHED SUCCESSFULLY!
================================================================================

📋 Running Components:
  🌐 Web Interface:      http://localhost:5000
  📊 Portfolio Monitor:  Running in separate terminal
  💰 Trading Mode:       📝 PAPER TRADING

🎯 Quick Actions:
  • Open web interface:  http://localhost:5000
  • Execute manual trade: python3 execute_trade.py
  • View logs:           tail -f trading_bot.log

⚠️  To stop all components:
  • Press Ctrl+C in this terminal
  • Close the portfolio monitor terminal

🎉 Happy Trading!

────────────────────────────────────────────────────────────────────────────────
Press Ctrl+C to shutdown...
```

### Portfolio Monitor Terminal
```
================================================================================
                     📊 REAL-TIME PORTFOLIO MONITOR
================================================================================

📈 ACCOUNT SUMMARY
  Portfolio Value:          $100,000.00
  Cash:                     $100,000.00
  Buying Power:             $200,000.00

💰 SESSION PERFORMANCE
  Starting Value:           $100,000.00
  Current Value:            $100,000.00
  Session P&L:              $0.00 (+0.00%)

📊 POSITIONS (0 active)
  No open positions

Last Updated: 2026-04-30 05:39:33 | Refresh: 5s | Press Ctrl+C to exit
```

### Browser (Web Interface)
- Trading dashboard opens automatically
- Click "Connect to Alpaca" to authenticate
- Start trading through the web interface

## 🛑 How to Stop Everything

### Option 1: Graceful Shutdown
1. Go to the **main launcher terminal**
2. Press `Ctrl+C`
3. Wait for shutdown message
4. Close portfolio monitor terminal manually

### Option 2: Force Stop
- Close all terminal windows
- Web server stops automatically

## 📁 Files Created

| File | Purpose |
|------|---------|
| `LAUNCH_ALL.py` | Master launcher (Python) |
| `LAUNCH_ALL.bat` | Windows launcher script |
| `LAUNCH_ALL.sh` | Linux/Mac launcher script |
| `run_trading_app.py` | Web server application |
| `portfolio_monitor.py` | Real-time portfolio display |
| `execute_trade.py` | Manual trade execution |

## 🎯 Components Launched

### 1. Web Server (Port 5000)
- **URL**: http://localhost:5000
- **Purpose**: Trading interface + API
- **Features**:
  - Account dashboard
  - Trade execution
  - Position tracking
  - Circuit breaker controls

### 2. Portfolio Monitor (New Terminal)
- **Purpose**: Real-time portfolio tracking
- **Updates**: Every 5 seconds
- **Shows**:
  - Portfolio value
  - Cash balance
  - All positions
  - Profit/loss
  - Market status

### 3. Browser (Auto-Opens)
- **URL**: http://localhost:5000
- **Purpose**: User interface
- **Actions**:
  - Connect to Alpaca
  - Execute trades
  - Monitor positions
  - View performance

## ⚙️ Configuration

All settings are loaded from `.env`:

```env
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
ENABLE_PAPER_TRADING=True
FLASK_PORT=5000
```

## 🔧 Troubleshooting

### Launcher Won't Start

**Problem**: "Python not found"
```bash
# Install Python 3.8+
# Windows: Download from python.org
# Linux: sudo apt install python3
# Mac: brew install python3
```

**Problem**: ".env file not found"
```bash
# Copy example file
cp .env.example .env
# Edit with your API keys
nano .env
```

**Problem**: "Port 5000 already in use"
```bash
# Change port in .env
FLASK_PORT=5001
```

### Portfolio Monitor Doesn't Open

**Linux**: No terminal emulator found
```bash
# Install a terminal emulator
sudo apt install gnome-terminal
# Or run manually
python3 portfolio_monitor.py
```

**Mac**: Terminal doesn't open
```bash
# Run manually in new terminal
python3 portfolio_monitor.py
```

### Browser Doesn't Open

```bash
# Manually open
http://localhost:5000
```

## 💡 Tips

1. **First Time Setup**
   - Make sure `.env` is configured
   - Run `pip install -r requirements.txt`
   - Test with `python3 test_env.py`

2. **During Trading**
   - Keep both terminals visible
   - Watch portfolio monitor for real-time updates
   - Use web interface for trading

3. **Stopping**
   - Always use Ctrl+C for clean shutdown
   - Check logs if something goes wrong
   - Portfolio monitor can run independently

## 🎉 Advantages

✅ **One Command** - Everything starts automatically
✅ **No Manual Setup** - Checks requirements automatically
✅ **Clean Shutdown** - Ctrl+C stops everything gracefully
✅ **Multi-Platform** - Works on Windows, Linux, Mac
✅ **Error Handling** - Shows clear error messages
✅ **Auto-Browser** - Opens interface automatically
✅ **Dual Display** - Terminal monitor + web interface

## 📊 Comparison

### Before (Manual)
```bash
# Terminal 1
python3 api_server.py

# Terminal 2
python3 portfolio_monitor.py

# Browser
# Manually open http://localhost:5000
```

### After (One-Click)
```bash
# Just one command!
./LAUNCH_ALL.sh

# Everything starts automatically:
# ✓ Web server
# ✓ Portfolio monitor
# ✓ Browser opens
```

## 🚀 Quick Start

```bash
# 1. Configure API keys
cp .env.example .env
nano .env

# 2. Launch everything
./LAUNCH_ALL.sh

# 3. Start trading!
# Browser opens automatically
# Portfolio monitor shows real-time updates
```

## 🎯 You're Ready!

The master launcher makes it incredibly easy to start trading:
- **One command** launches everything
- **Automatic checks** ensure everything is configured
- **Clean interface** shows what's running
- **Easy shutdown** with Ctrl+C

Happy Trading! 📈
