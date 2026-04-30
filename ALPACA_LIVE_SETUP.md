# Alpaca Live Paper Trading Setup Guide

## 🎯 Goal
Set up real paper trading with Alpaca API so you can see live trades on the Alpaca website and in your dashboard.

## 📋 Step-by-Step Instructions

### Step 1: Get Your Alpaca API Keys

1. **Go to Alpaca Markets**: https://alpaca.markets
2. **Sign up for a free account** (if you don't have one)
3. **Log in to your dashboard**: https://app.alpaca.markets/paper/dashboard/overview
4. **Navigate to API Keys**:
   - Click on your profile (top right)
   - Select "API Keys" or go to: https://app.alpaca.markets/paper/dashboard/api-keys
5. **Generate Paper Trading Keys**:
   - Click "Generate New Key"
   - Give it a name (e.g., "Trading Bot")
   - **IMPORTANT**: Copy both keys immediately (you won't see the secret key again!)
   - Save them somewhere secure

### Step 2: Configure Your .env File

Open your `.env` file and replace the placeholder values:

```bash
# Replace these lines:
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here

# With your actual keys:
ALPACA_API_KEY=PK1234567890ABCDEF  # Your actual key
ALPACA_SECRET_KEY=abcdef1234567890  # Your actual secret
```

**Make sure:**
- ✅ `ENABLE_PAPER_TRADING=True` (already set correctly)
- ✅ No extra spaces around the = sign
- ✅ No quotes around the keys
- ✅ Keys are on separate lines

### Step 3: Restart the API Server

1. **Stop the current server**:
   - Go to the terminal running `python3 api_server.py`
   - Press `Ctrl+C`

2. **Start it again**:
   ```bash
   python3 api_server.py
   ```

3. **Look for success message**:
   ```
   ✅ Successfully authenticated with Alpaca
   Account value: $100,000.00
   Buying power: $200,000.00
   Paper Trading: True
   ```

### Step 4: Open the Trading Dashboard

1. **Open `index.html` in your browser**
2. **Click "START TRADING"** button
3. **You should see**:
   - "✅ Connected to Alpaca Markets" in the trade log
   - Live portfolio value updating every 2 seconds
   - Real-time metrics

### Step 5: Verify on Alpaca Website

1. **Go to Alpaca Dashboard**: https://app.alpaca.markets/paper/dashboard/overview
2. **Check "Activity" tab**: You'll see your trades appear here
3. **Check "Positions" tab**: See your open positions
4. **Check "Orders" tab**: See all orders (filled, pending, cancelled)

## 🔍 What You'll See

### In Your Trading Dashboard (index.html):
- ✅ **Live Portfolio Value** - Updates every 2 seconds from Alpaca
- ✅ **Real Positions** - Shows actual holdings from your Alpaca account
- ✅ **Live Trades** - Real orders executed on Alpaca
- ✅ **Current Prices** - Real-time market data
- ✅ **P&L** - Actual profit/loss from your positions

### On Alpaca Website:
- ✅ **All trades appear in Activity feed**
- ✅ **Positions show in Positions tab**
- ✅ **Orders show in Orders tab**
- ✅ **Account value matches your dashboard**

## 🚀 Making Your First Trade

Once authenticated, the system will automatically:

1. **Analyze market conditions** using the selected algorithm (PPO/A2C/SAC)
2. **Generate trading signals** based on risk tolerance
3. **Execute trades** through Alpaca API
4. **Update your dashboard** in real-time
5. **Show trades on Alpaca website** immediately

### Manual Trading (Optional):

You can also manually execute trades using the risk management controls:

1. **Set Stop-Loss**:
   - Enter symbol (e.g., AAPL)
   - Enter stop price
   - Click "Set Stop-Loss"

2. **Set Take-Profit**:
   - Enter symbol
   - Enter limit price
   - Click "Set Take-Profit"

## ⚙️ Update Frequency Settings

### Current Settings:
- **Live Metrics**: Update every 2 seconds
- **Trading Decisions**: Based on "Execution Frequency" setting (default: 1 second)
- **Position Updates**: Every trading cycle

### To Change Update Speed:

**Option 1: Change in UI**
- Go to "Trading Configuration Panel"
- Change "Execution Frequency" dropdown
- Options: 0.5s, 1.0s, 2.0s

**Option 2: Change in Code (script.js)**
```javascript
// Find this line (around line 420):
setInterval(async () => {
    await updateLiveMetrics();
}, 2000); // Change 2000 to 1000 for 1-second updates

// For trading speed, change:
tradingSpeed: 1000  // milliseconds between trades
```

## 🛡️ Safety Features Active

Your system has these protections enabled:

1. **Circuit Breaker**:
   - Max 50 trades per day
   - Max 5% daily loss
   - Max 15% per position
   - Min $1,000 account balance

2. **Paper Trading Mode**:
   - No real money at risk
   - Full API features
   - Real market data
   - Practice safely

3. **Emergency Controls**:
   - Emergency Stop button
   - Close All Positions button
   - Manual circuit breaker reset

## 📊 Monitoring Your Trades

### Real-Time Dashboard Metrics:
- 💼 Portfolio Value (live)
- 📈 Total Return (live)
- 📉 Sharpe Ratio (calculated)
- ⚠️ Max Drawdown (tracked)
- ✅ Win Rate (calculated)
- 🔢 Total Trades (counted)

### Alpaca Website Monitoring:
- **Dashboard**: https://app.alpaca.markets/paper/dashboard/overview
- **Activity**: See all trades as they happen
- **Positions**: Monitor open positions
- **Orders**: Track order status
- **Account**: View account summary

## 🔧 Troubleshooting

### "Authentication failed" Error:
- ✅ Check API keys are correct in `.env`
- ✅ Ensure no extra spaces or quotes
- ✅ Verify keys are for Paper Trading (not Live)
- ✅ Restart the server after changing `.env`

### "Not authenticated" in Dashboard:
- ✅ Click "START TRADING" button
- ✅ Check browser console for errors (F12)
- ✅ Verify server is running
- ✅ Check API server terminal for error messages

### Trades Not Appearing on Alpaca:
- ✅ Verify you're logged into Paper Trading account
- ✅ Check the correct account (Paper vs Live)
- ✅ Refresh the Alpaca dashboard
- ✅ Check "Activity" tab for recent trades

### Live Updates Not Working:
- ✅ Ensure you clicked "START TRADING"
- ✅ Check browser console (F12) for errors
- ✅ Verify API server is responding (check terminal)
- ✅ Try refreshing the page

## 📝 Current Status Check

Run this checklist:

- [ ] Alpaca account created
- [ ] API keys generated
- [ ] Keys added to `.env` file
- [ ] Server restarted
- [ ] Authentication successful (check terminal)
- [ ] Dashboard opened in browser
- [ ] "START TRADING" clicked
- [ ] Live metrics updating
- [ ] Trades appearing on Alpaca website

## 🎯 Expected Behavior

Once everything is set up correctly:

1. **Every 2 seconds**: Dashboard polls `/api/metrics/live` for updated portfolio data
2. **Every 1 second** (default): System evaluates trading opportunities
3. **When trade executes**: 
   - Order sent to Alpaca API
   - Trade appears in your dashboard log
   - Trade appears on Alpaca website
   - Position updates in real-time
   - Metrics recalculate automatically

## 🚨 Important Notes

1. **Paper Trading Only**: Your `.env` has `ENABLE_PAPER_TRADING=True` - this is correct!
2. **No Real Money**: Paper trading uses virtual money ($100,000 default)
3. **Real Market Data**: Prices and execution are realistic
4. **Safe Testing**: Perfect for testing strategies
5. **Alpaca Sync**: All trades sync with Alpaca website in real-time

## 📞 Need Help?

If you're still having issues:

1. **Check the terminal** where `api_server.py` is running for error messages
2. **Check browser console** (F12) for JavaScript errors
3. **Verify API keys** are correct and for Paper Trading
4. **Check Alpaca status**: https://status.alpaca.markets

## ✅ Success Indicators

You'll know it's working when you see:

### In Terminal:
```
✅ Successfully authenticated with Alpaca
Account value: $100,000.00
Buying power: $200,000.00
Paper Trading: True
```

### In Browser Dashboard:
```
✅ Connected to Alpaca Markets
🚐 Trading system started
```

### On Alpaca Website:
- Trades appearing in Activity feed
- Positions showing in Positions tab
- Account value changing with trades

---

## 🎉 You're Ready!

Once you see these success indicators, your system is fully operational with:
- ✅ Real Alpaca API integration
- ✅ Live portfolio updates every 2 seconds
- ✅ Real trades visible on Alpaca website
- ✅ Full risk management controls
- ✅ Circuit breaker protection

Happy trading! 🚀
