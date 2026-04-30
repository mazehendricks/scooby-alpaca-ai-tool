# 🚀 Quick Start Guide - Single File Application

## Overview

The **`run_trading_app.py`** file is a complete, standalone trading application that includes everything you need in one file:

- ✅ Alpaca API client
- ✅ Circuit breaker safety system
- ✅ Flask web server
- ✅ All API endpoints
- ✅ Configuration management
- ✅ Logging system

## 🎯 How to Run

### Option 1: One-Click Launchers (Easiest)

#### Windows:
```
Double-click: START_TRADING.bat
```

#### Linux/Mac:
```bash
./START_TRADING.sh
```

### Option 2: Direct Python Execution

```bash
python3 run_trading_app.py
```

### Option 3: Make it Executable (Linux/Mac)

```bash
chmod +x run_trading_app.py
./run_trading_app.py
```

## 📋 What Happens When You Run It

1. **Loads Configuration** from `.env` file
2. **Initializes Safety Systems** (circuit breaker)
3. **Starts Web Server** on port 5000
4. **Opens Browser** automatically to http://localhost:5000
5. **Ready to Trade!**

## 🖥️ Application Output

When you run the application, you'll see:

```
======================================================================
🚀 ALPACA TRADING BOT - ALL-IN-ONE APPLICATION
======================================================================

📊 Configuration:
   • Paper Trading: True
   • API Endpoint: https://paper-api.alpaca.markets
   • Port: 5000
   • Max Daily Trades: 50
   • Max Position Size: 15.0%
   • Max Daily Loss: 5.0%

🌐 Starting web server...
   • Local: http://localhost:5000
   • Network: http://127.0.0.1:5000

⚠️  Press Ctrl+C to stop the server
======================================================================
```

## 🎮 Using the Application

1. **Browser Opens Automatically** to the trading interface
2. **Click "Connect to Alpaca"** to authenticate
3. **View Your Portfolio** - real-time balance and positions
4. **Execute Trades** - buy/sell stocks with safety checks
5. **Monitor Performance** - track P&L and trade history

## 🛡️ Built-in Safety Features

The single file includes all safety features:

- ✅ **Circuit Breaker** - prevents excessive losses
- ✅ **Position Size Limits** - max 15% per position
- ✅ **Daily Trade Limits** - max 50 trades per day
- ✅ **Daily Loss Limits** - stops at 5% daily loss
- ✅ **Minimum Balance Protection** - maintains $1,000 minimum
- ✅ **Paper Trading Mode** - safe testing environment

## 📁 File Structure

```
run_trading_app.py          # ← EVERYTHING IN ONE FILE!
├── Configuration
├── Logging Setup
├── Circuit Breaker Class
├── Alpaca Client Class
├── Flask Web Application
└── Main Entry Point

START_TRADING.bat           # Windows launcher
START_TRADING.sh            # Linux/Mac launcher
index.html                  # Web interface (required)
style.css                   # Styling (required)
script.js                   # Frontend logic (required)
.env                        # Your API keys (required)
```

## ⚙️ Configuration

All settings are loaded from `.env`:

```env
ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
ENABLE_PAPER_TRADING=True
FLASK_PORT=5000
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE_PERCENT=15.0
MAX_DAILY_LOSS_PERCENT=5.0
MIN_ACCOUNT_BALANCE=1000.0
```

## 🔧 Customization

Edit `run_trading_app.py` to customize:

- **Port**: Change `PORT` in Config class
- **Safety Limits**: Modify circuit breaker parameters
- **Logging**: Adjust `LOG_LEVEL` (DEBUG, INFO, WARNING, ERROR)
- **API Endpoints**: Add new Flask routes
- **Trading Logic**: Extend AlpacaClient class

## 📊 API Endpoints

The single file provides these endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve web interface |
| `/api/login` | POST | Authenticate with Alpaca |
| `/api/logout` | POST | Disconnect from Alpaca |
| `/api/account` | GET | Get account summary |
| `/api/positions` | GET | Get current positions |
| `/api/price/<symbol>` | GET | Get stock price |
| `/api/trade` | POST | Execute buy/sell order |
| `/api/circuit-breaker/status` | GET | Get safety status |
| `/api/circuit-breaker/reset` | POST | Reset circuit breaker |
| `/api/health` | GET | Health check |

## 🐛 Troubleshooting

### Application Won't Start

```bash
# Check Python version (need 3.8+)
python3 --version

# Install dependencies
pip3 install -r requirements.txt

# Check .env file exists
ls -la .env
```

### Can't Connect to Alpaca

1. Verify API keys in `.env`
2. Check paper trading setting matches your keys
3. Ensure internet connection is active
4. Check Alpaca API status

### Port Already in Use

Change port in `.env`:
```env
FLASK_PORT=5001
```

## 🎯 Advantages of Single File

✅ **Easy to Deploy** - just copy one file
✅ **No Import Issues** - everything is self-contained
✅ **Easy to Understand** - all code in one place
✅ **Portable** - works anywhere Python runs
✅ **Simple Debugging** - one file to check
✅ **Quick Modifications** - edit and run immediately

## 🔒 Security Notes

- ⚠️ Never commit `.env` to version control
- ⚠️ Keep API keys secure
- ⚠️ Start with paper trading
- ⚠️ Test thoroughly before live trading
- ⚠️ Monitor logs in `trading_bot.log`

## 📝 Logs

Application logs are saved to:
- **Console Output** - real-time activity
- **trading_bot.log** - persistent log file

## 🚦 Status Indicators

- 🟢 **Green** - System operational
- 🟡 **Yellow** - Warning/caution
- 🔴 **Red** - Error/stopped
- 📝 **Paper** - Paper trading mode
- 💰 **Live** - Live trading mode

## 💡 Tips

1. **Always start with paper trading**
2. **Monitor the circuit breaker status**
3. **Check logs regularly**
4. **Test with small positions first**
5. **Keep browser console open for debugging**

## 🆘 Support

If you encounter issues:

1. Check `trading_bot.log` for errors
2. Verify `.env` configuration
3. Test API connection with `test_env.py`
4. Review circuit breaker status
5. Check Alpaca API documentation

## 🎉 You're Ready!

Run the application and start trading safely with built-in protections!

```bash
python3 run_trading_app.py
```

Happy Trading! 📈
