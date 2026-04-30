# 🚀 Quick Start Guide

Get up and running with the AI Trading Bot using Alpaca in 5 minutes!

## ⚡ Fast Setup

### Step 1: Create Alpaca Account (2 minutes)

1. Sign up at [https://alpaca.markets](https://alpaca.markets)
2. Verify your email
3. Get your **Paper Trading API keys** from the dashboard

### Step 2: Install Dependencies (2 minutes)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Step 3: Configure Credentials (1 minute)

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Open `.env` file in a text editor
3. Add your Alpaca API credentials:

```env
# Get these from: https://app.alpaca.markets/paper/dashboard/overview
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# IMPORTANT: Keep paper trading enabled for testing!
ENABLE_PAPER_TRADING=True
```

💡 **Need help getting API keys?** See [ALPACA_SETUP.md](ALPACA_SETUP.md) for detailed instructions.

### Step 4: Start Trading (1 minute)

**Linux/macOS:**
```bash
./start_server.sh
```

**Windows:**
```cmd
start_server.bat
```

**Or manually:**
```bash
source venv/bin/activate  # Activate virtual environment
python api_server.py      # Start server
```

### Step 5: Open Web Interface

1. Open [`index.html`](index.html) in your browser
2. Click **"Start Simulation"**
3. Watch your AI trade! 🤖📈

## 🎯 What You'll See

### Server Console
```
============================================================
🤖 AI Trading Bot API Server Starting (Alpaca)
============================================================
Starting API server on port 5000
Trading Platform: Alpaca Markets
Paper Trading Mode: True
✅ Successfully authenticated with Alpaca
Account value: $100,000.00
Buying power: $100,000.00
```

### Web Interface
- Real-time portfolio value
- Current holdings with P&L
- Trade execution log
- AI decision explanations
- Circuit breaker status
- Market status (open/closed)

## 🧪 Testing Checklist

- [ ] Server starts without errors
- [ ] Authentication succeeds
- [ ] "Paper Trading Mode" is active
- [ ] Account shows $100,000 virtual balance
- [ ] Trades execute successfully
- [ ] Circuit breaker is active
- [ ] Emergency stop button works

## ⚠️ Important Notes

### Paper Trading Mode
- **Enabled by default** for safety
- Gives you **$100,000 virtual money**
- Uses **real market data** and prices
- Simulates trades without real money
- Perfect for testing algorithms
- Shows what would happen in real trading

### Safety Features
- **Circuit Breaker**: Stops trading if limits exceeded
- **Daily Trade Limit**: Max 50 trades per day (configurable)
- **Position Size Limit**: Max 15% per position (configurable)
- **Daily Loss Limit**: Stops if loss exceeds 5% (configurable)
- **Emergency Stop**: Manual override button

### Before Real Trading

⚠️ **DO NOT disable paper trading until:**
1. ✅ You've tested thoroughly (minimum 1-2 weeks)
2. ✅ You understand all algorithms (PPO, A2C, SAC)
3. ✅ You've reviewed all safety limits
4. ✅ You're comfortable with potential losses
5. ✅ You've read all documentation
6. ✅ You start with small amounts

## 🐛 Common Issues

### "Backend server not running"
**Fix:** Make sure [`api_server.py`](api_server.py) is running in a terminal

### "Authentication failed"
**Fix:** 
- Check credentials in [`.env`](.env) file
- Verify you're using **Paper Trading** API keys (start with `PK...`)
- Regenerate keys if needed from Alpaca dashboard

### "Module not found: alpaca_trade_api"
**Fix:** 
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### "Port 5000 already in use"
**Fix:** Change `FLASK_PORT` in [`.env`](.env) or stop other services on port 5000

### "Could not fetch price for SYMBOL"
**Fix:**
- Check if market is open (US market hours: 9:30 AM - 4:00 PM ET)
- Verify symbol is valid (Alpaca supports US stocks only)
- Some stocks may not be tradeable

## 🦙 Why Alpaca?

Alpaca is **perfect for algorithmic trading** because:

- ✅ **Commission-free** trading
- ✅ **No minimum balance** required
- ✅ **Built for developers** with excellent API
- ✅ **Paper trading** included for free
- ✅ **Real-time market data**
- ✅ **Well-documented** Python SDK
- ✅ **200 API requests per minute**
- ✅ **Active community** and support

## 📚 Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **Configure Alpaca properly**: [ALPACA_SETUP.md](ALPACA_SETUP.md)
3. **Understand the algorithms**: See README Algorithm Details section
4. **Customize safety limits**: Edit [`.env`](.env) file
5. **Monitor performance**: Watch the dashboard metrics
6. **Test different strategies**: Try PPO, A2C, and SAC algorithms

## 🎓 Learning Resources

### Alpaca Documentation
- [Alpaca API Docs](https://alpaca.markets/docs/)
- [Python SDK Guide](https://github.com/alpacahq/alpaca-trade-api-python)
- [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard/overview)

### Project Documentation
- [ALPACA_SETUP.md](ALPACA_SETUP.md) - Detailed setup guide
- [README.md](README.md) - Complete documentation
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Architecture overview

## 🆘 Need Help?

- **Detailed Setup**: See [ALPACA_SETUP.md](ALPACA_SETUP.md)
- **Full Documentation**: See [README.md](README.md)
- **Troubleshooting**: Check server logs and [`trading_bot.log`](trading_bot.log)
- **Alpaca Support**: [https://alpaca.markets/support](https://alpaca.markets/support)
- **Community**: [Alpaca Slack](https://alpaca.markets/community)

## ⚖️ Legal Disclaimer

This software is for **educational purposes only**. Trading involves substantial risk of loss. The authors are not responsible for any financial losses. Always consult with qualified financial advisors before making investment decisions.

**Pattern Day Trading Rule**: If you make 4+ day trades within 5 business days, you need $25,000 minimum balance (applies to live trading only).

**USE AT YOUR OWN RISK.**

---

## 🎉 You're Ready!

Your AI Trading Bot is now configured with Alpaca Markets!

**Next:** Open [`index.html`](index.html) and click "Start Simulation" to begin trading with $100,000 virtual money.

**Happy Trading! 🚀📈**

Remember: Start with paper trading, test thoroughly, and never risk more than you can afford to lose!
