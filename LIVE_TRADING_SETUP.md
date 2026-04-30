# 🚀 Live Paper Trading Setup Guide

## Overview

Your Alpaca AI Trading System is now configured for **LIVE PAPER TRADING** mode. This means:
- ✅ Real Alpaca Paper Trading API integration
- ✅ Real-time market data
- ✅ Actual API endpoints and responses
- ✅ Live portfolio tracking
- ✅ Real order execution (paper money only)
- ❌ NO real money at risk

---

## 📋 Prerequisites

1. **Alpaca Account** - Sign up at [alpaca.markets](https://alpaca.markets)
2. **Paper Trading API Keys** - Get from your Alpaca dashboard
3. **Python 3.7+** installed
4. **API Server Running** on port 5000

---

## 🔑 Step 1: Get Your Alpaca API Keys

### 1. Create Alpaca Account
1. Go to [https://alpaca.markets](https://alpaca.markets)
2. Click **"Sign Up"**
3. Complete registration
4. Verify your email

### 2. Get Paper Trading Keys
1. Log into your Alpaca dashboard
2. Navigate to **"Paper Trading"** section
3. Click **"View API Keys"** or **"Generate New Keys"**
4. Copy both:
   - **API Key ID** (starts with `PK...`)
   - **Secret Key** (starts with `...`)

⚠️ **IMPORTANT**: These are PAPER TRADING keys - they use fake money!

---

## ⚙️ Step 2: Configure Your System

### Option A: Using Environment Variables (Recommended)

1. **Create `.env` file** in project root:
```bash
cp env.example .env
```

2. **Edit `.env` file**:
```env
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### Option B: Direct Configuration

1. **Edit `config.py`**:
```python
# Alpaca API Configuration
ALPACA_API_KEY = "PKxxxxxxxxxxxxxxxxxx"
ALPACA_SECRET_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
ALPACA_BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading
```

⚠️ **Security Note**: Never commit real API keys to version control!

---

## 🚀 Step 3: Start the System

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start API Server
```bash
python3 api_server.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Alpaca Paper Trading API initialized
 * Circuit breaker active
```

### 3. Open Web Interface
```bash
# Open in your browser
open index.html
# Or just double-click index.html
```

---

## 🖥️ Step 4: Using the Live Console

### What You'll See in the Console:

#### System Startup:
```
[00:00:00] [SYSTEM] 🚀 Alpaca AI Trading System Initialized
[00:00:01] [SYSTEM] Checking server health...
[00:00:01] [API] → GET /health
[00:00:01] [API] ← GET /health [200] 45ms
[00:00:02] [API] → GET /auth/status
[00:00:02] [API] ← GET /auth/status [200] 32ms
```

#### Authentication:
```
[00:00:05] [API] → POST /auth/login
[00:00:05] [API] ← POST /auth/login [200] 234ms
[00:00:05] [SYSTEM] ✅ Connected to Alpaca Paper Trading API
```

#### Live Metrics Updates:
```
[00:00:10] [API] → GET /metrics/live
[00:00:10] [API] ← GET /metrics/live [200] 156ms
[00:00:10] [API] Live metrics - Portfolio: $100000.00, Return: +2.34%
```

#### Trading Activity:
```
[00:01:23] [DECISION] AI analyzing market... Action: BUY | Symbol: AAPL | Confidence: 0.87
[00:01:23] [TRADE] 🟢 BUY 10 shares of AAPL @ confidence 0.87
[00:01:23] [API] → POST /trade/execute
[00:01:24] [API] ← POST /trade/execute [200] 445ms
```

#### Position Updates:
```
[00:02:00] [API] → GET /account/positions
[00:02:00] [API] ← GET /account/positions [200] 123ms
[00:02:00] [API] Loaded 3 open position(s)
```

---

## 📊 Real-Time API Endpoint Monitoring

### All API Calls Are Logged:

| Endpoint | Method | Purpose | Frequency |
|----------|--------|---------|-----------|
| `/health` | GET | Server health check | On startup |
| `/auth/status` | GET | Check authentication | On startup |
| `/auth/login` | POST | Authenticate with Alpaca | On startup |
| `/metrics/live` | GET | Get live portfolio metrics | Every 2 seconds |
| `/account/portfolio` | GET | Get portfolio value | On demand |
| `/account/positions` | GET | Get open positions | Every trade cycle |
| `/trade/execute` | POST | Execute trade | When AI decides |
| `/risk/limits` | POST | Update risk limits | When changed |
| `/risk/stop-loss` | POST | Set stop-loss order | When set |
| `/risk/take-profit` | POST | Set take-profit order | When set |
| `/risk/close-all` | POST | Close all positions | Emergency |
| `/circuit-breaker/emergency-stop` | POST | Emergency stop | When triggered |
| `/circuit-breaker/reset` | POST | Reset circuit breaker | After stop |

### Console Shows:
- **→** Outgoing request with method and endpoint
- **←** Response with status code and duration
- **Response data** (when verbose mode enabled)
- **Errors** with full details

---

## 🎯 Testing Your Setup

### 1. Verify Connection
1. Open the web interface
2. Check console for:
   ```
   [SYSTEM] ✅ Connected to Alpaca Paper Trading API
   ```
3. If you see authentication errors, check your API keys

### 2. Test Trading
1. Click **"START TRADING"**
2. Watch console for:
   - API calls to `/metrics/live`
   - Trading decisions
   - Position updates
3. Monitor portfolio value changes

### 3. Test Risk Management
1. Click **"Update Limits"** button
2. Console should show:
   ```
   [API] → POST /risk/limits
   [API] ← POST /risk/limits [200] 89ms
   ```

### 4. Test Emergency Stop
1. Click **"EMERGENCY STOP"**
2. Console should show:
   ```
   [SYSTEM] 🚨 EMERGENCY STOP ACTIVATED
   [API] → POST /circuit-breaker/emergency-stop
   ```

---

## 🔍 Verbose Mode

### Enable Detailed Logging:
1. Check **"Verbose Mode"** checkbox in console controls
2. You'll see full API responses:
   ```
   [API] Response: {"portfolio_value":100234.56,"total_return":234.56,...}
   ```

### Disable for Cleaner View:
- Uncheck "Verbose Mode" to see only key events

---

## 🐛 Troubleshooting

### Problem: "Cannot connect to API server"
**Solution:**
1. Check if `api_server.py` is running
2. Verify it's on port 5000
3. Check console for errors:
   ```bash
   python3 api_server.py
   ```

### Problem: "Authentication failed"
**Solution:**
1. Verify API keys in `config.py` or `.env`
2. Ensure keys are for **Paper Trading** (start with `PK`)
3. Check Alpaca dashboard for key status
4. Console will show:
   ```
   [API] Authentication failed: unauthorized
   ```

### Problem: "No trades executing"
**Solution:**
1. Check if trading is started (click START TRADING)
2. Verify authentication succeeded
3. Check risk tolerance (higher = more trades)
4. Look for errors in console

### Problem: "API calls timing out"
**Solution:**
1. Check internet connection
2. Verify Alpaca API status: [status.alpaca.markets](https://status.alpaca.markets)
3. Console will show timeout errors

---

## 📈 Understanding the Data Flow

### 1. Startup Sequence:
```
Browser → API Server → Alpaca API
   ↓
Console logs each step
   ↓
Authentication complete
   ↓
Live updates begin
```

### 2. Trading Cycle:
```
AI Decision → API Server → Alpaca API
     ↓            ↓            ↓
  Console    Validation   Execution
     ↓            ↓            ↓
  Display ← Response ← Confirmation
```

### 3. Real-Time Updates:
```
Every 2 seconds:
  → GET /metrics/live
  ← Portfolio data
  → Update UI
  → Log to console
```

---

## 🎨 Console Features

### Color Coding:
- **🟢 Green** - Successful operations, trades
- **🔴 Red** - Errors, failures
- **🟡 Yellow** - Warnings, important notices
- **🔵 Blue** - Information, user actions
- **🟣 Purple** - API calls and responses

### Controls:
- **Clear Console** - Remove all log entries
- **Auto-Scroll** - Toggle automatic scrolling
- **Verbose Mode** - Show/hide detailed responses

### Timestamps:
- Every log entry has precise timestamp
- Format: `[HH:MM:SS]`

---

## 💡 Pro Tips

### 1. Monitor API Performance
- Watch response times in console
- Typical: 50-200ms for most calls
- Slow responses (>500ms) may indicate issues

### 2. Track Your Trades
- Console shows every trade with full details
- Use verbose mode to see order IDs
- Cross-reference with Alpaca dashboard

### 3. Debug Issues
- Enable verbose mode
- Check for error patterns
- Look for failed API calls

### 4. Optimize Trading
- Monitor decision frequency
- Adjust risk tolerance based on activity
- Watch for circuit breaker triggers

---

## 🔐 Security Best Practices

### 1. Protect Your Keys
- Never share API keys
- Don't commit to Git
- Use environment variables
- Rotate keys periodically

### 2. Use Paper Trading
- Test strategies with paper money first
- Verify everything works correctly
- Only switch to live when confident

### 3. Monitor Activity
- Watch console for unusual activity
- Check Alpaca dashboard regularly
- Set up alerts for large losses

---

## 📚 Additional Resources

- **Alpaca Docs**: [alpaca.markets/docs](https://alpaca.markets/docs)
- **API Reference**: [alpaca.markets/docs/api-references](https://alpaca.markets/docs/api-references)
- **Paper Trading**: [alpaca.markets/docs/trading/paper-trading](https://alpaca.markets/docs/trading/paper-trading)
- **Status Page**: [status.alpaca.markets](https://status.alpaca.markets)

---

## 🎉 You're Ready!

Your system is now configured for **LIVE PAPER TRADING** with:
- ✅ Real Alpaca API integration
- ✅ Real-time endpoint monitoring
- ✅ Complete console logging
- ✅ Full transparency of all operations
- ✅ Safe paper trading environment

**Start trading and watch the console to see everything happening in real-time!** 🚀📈💰
