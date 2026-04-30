# 📝 Alpaca Paper Trading - Live Updates Setup

## ✅ What's Been Updated

Your system is now configured for **REAL Alpaca paper trading** with live updates every second!

### Key Changes Made:

1. **✅ Removed All Simulated Trading**
   - Eliminated fake trading logic from [`script.js`](script.js)
   - All data now comes directly from Alpaca API
   - No more random number generation for portfolio values

2. **✅ Live Updates Every 1 Second**
   - Portfolio metrics refresh automatically every 1 second
   - Position data updates in real-time
   - Numbers animate when they change for visual feedback

3. **✅ CSS Animations Added**
   - Values flash with a blue highlight when updated
   - Smooth transitions for all number changes
   - Live indicator pulse animation

4. **✅ Initial Capital Set to $10**
   - Starting balance is now $10 (perfect for testing)
   - Minimum capital reduced to $10
   - All default values updated

---

## 🚀 How to Use

### Step 1: Configure Your Alpaca API Keys

Edit your [`.env`](.env) file with your Alpaca paper trading credentials:

```bash
ALPACA_API_KEY=your_paper_trading_api_key_here
ALPACA_SECRET_KEY=your_paper_trading_secret_key_here
ENABLE_PAPER_TRADING=True
```

**Get your keys here:** https://app.alpaca.markets/paper/dashboard/overview

### Step 2: Start the API Server

The server is already running! If you need to restart it:

```bash
python3 api_server.py
```

You should see:
```
🤖 AI Trading Bot API Server Starting (Alpaca)
✅ Successfully authenticated with Alpaca
Account value: $10.00
Paper Trading: True
```

### Step 3: Open the Web Interface

Open [`index.html`](index.html) in your browser or use Live Server in VS Code.

### Step 4: Start Trading

1. **Click "START TRADING"** - This will:
   - Authenticate with Alpaca
   - Start live updates every 1 second
   - Display real portfolio data

2. **Watch the Numbers Move!** 
   - Portfolio value updates every second
   - Position values change in real-time
   - Numbers flash blue when they update
   - All data comes from Alpaca API

---

## 📊 What You'll See

### Live Metrics (Updates Every 1 Second):
- **Portfolio Value** - Your total account value from Alpaca
- **Total Return** - Profit/loss since you started
- **Sharpe Ratio** - Risk-adjusted return metric
- **Max Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of profitable trades
- **Total Trades** - Number of executed trades

### Real-Time Position Data:
- Symbol, quantity, average price
- Current price (live from Alpaca)
- Current value and P&L
- Portfolio allocation percentage

---

## 🎯 How to Trade

### Manual Trading:

You can execute trades through the API or by adding trade buttons to the UI.

**Example: Buy Stock via API**
```bash
curl -X POST http://localhost:5000/api/trade/buy \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "quantity": 1}'
```

**Example: Sell Stock via API**
```bash
curl -X POST http://localhost:5000/api/trade/sell \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "quantity": 1}'
```

### Automated Trading:

The system is set up for monitoring only. To add automated trading:
1. Implement your trading strategy in [`script.js`](script.js)
2. Call the buy/sell API endpoints based on your signals
3. All trades will execute through Alpaca paper trading

---

## 🔒 Safety Features

### Circuit Breaker Protection:
- **Max Daily Trades**: 50 trades per day
- **Max Daily Loss**: 5% of portfolio
- **Max Position Size**: 15% of portfolio per stock
- **Min Account Balance**: $1,000 minimum

### Emergency Stop:
Click the **"EMERGENCY STOP"** button to immediately halt all trading.

---

## 🎨 Visual Features

### Animations:
- **Value Update Flash** - Blue highlight when numbers change
- **Live Indicator** - Pulsing green dot shows active connection
- **Smooth Transitions** - All changes animate smoothly

### Color Coding:
- 🟢 **Green** - Positive returns, profitable positions
- 🔴 **Red** - Negative returns, losing positions
- 🟡 **Yellow** - Warnings, paused state
- 🔵 **Blue** - Active updates, information

---

## 📈 API Endpoints

All endpoints are available at `http://localhost:5000/api/`

### Account:
- `GET /account/summary` - Full account details
- `GET /account/portfolio` - Portfolio value and buying power
- `GET /account/positions` - Current positions

### Trading:
- `POST /trade/buy` - Execute buy order
- `POST /trade/sell` - Execute sell order

### Market Data:
- `GET /market/quote/<symbol>` - Get stock quote
- `GET /market/price/<symbol>` - Get current price
- `GET /market/status` - Market open/closed status

### Live Metrics:
- `GET /metrics/live` - Real-time portfolio metrics (used by frontend)
- `GET /metrics/performance` - Detailed performance analysis

### Risk Management:
- `GET /risk/limits` - Current risk limits
- `POST /risk/limits` - Update risk limits
- `POST /risk/stop-loss` - Set stop-loss order
- `POST /risk/take-profit` - Set take-profit order
- `POST /risk/close-all` - Emergency close all positions

---

## 🐛 Troubleshooting

### Numbers Not Updating?
1. Check that the API server is running
2. Open browser console (F12) and look for errors
3. Verify your Alpaca API keys are correct
4. Make sure you're authenticated (click START TRADING)

### "Not authenticated" Error?
1. Check your `.env` file has valid API keys
2. Restart the API server
3. Click START TRADING to authenticate

### No Positions Showing?
- You need to execute trades first
- Positions will appear after you buy stocks
- Use the API endpoints or add trade buttons to the UI

---

## 📝 Important Notes

### Paper Trading vs Live Trading:
- ✅ **Currently using PAPER TRADING** (safe, no real money)
- ⚠️ **Never use live trading without thorough testing**
- 🔒 **Keep `ENABLE_PAPER_TRADING=True` in `.env`**

### Data Updates:
- Portfolio metrics update every **1 second**
- Position data updates every **1 second**
- Market data is real-time from Alpaca
- All values come from actual Alpaca API (no simulation)

### Starting Balance:
- Default starting capital: **$10**
- Alpaca paper trading gives you $100,000 virtual money
- The $10 setting is just for the UI display
- Your actual Alpaca paper account balance will be used

---

## 🎓 Next Steps

1. **Test with Small Trades**: Start with 1-2 shares to see the system work
2. **Watch Live Updates**: Observe how numbers change every second
3. **Implement Strategy**: Add your trading logic to [`script.js`](script.js)
4. **Monitor Performance**: Use the metrics dashboard to track results
5. **Adjust Risk Limits**: Configure circuit breaker settings as needed

---

## 📚 Related Documentation

- [`ALPACA_LIVE_SETUP.md`](ALPACA_LIVE_SETUP.md) - Alpaca setup guide
- [`LIVE_UPDATES_FEATURES.md`](LIVE_UPDATES_FEATURES.md) - Live update features
- [`VIEWING_OPTIONS.md`](VIEWING_OPTIONS.md) - Viewing options guide
- [`README.md`](README.md) - Main project documentation

---

## ⚡ Quick Reference

**Start Server:**
```bash
python3 api_server.py
```

**Execute Trade:**
```bash
curl -X POST http://localhost:5000/api/trade/buy \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "quantity": 1}'
```

**Check Portfolio:**
```bash
curl http://localhost:5000/api/account/portfolio
```

**View Positions:**
```bash
curl http://localhost:5000/api/account/positions
```

---

## 🎉 You're All Set!

Your system is now configured for **real Alpaca paper trading** with **live updates every second**. 

Open [`index.html`](index.html) in your browser, click **START TRADING**, and watch your portfolio update in real-time! 🚀

**Happy Trading! 📈**
