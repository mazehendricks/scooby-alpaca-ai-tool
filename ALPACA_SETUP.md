# 🦙 Alpaca Setup Guide

Complete guide to setting up your AI Trading Bot with Alpaca Markets.

## 📋 Table of Contents

1. [Why Alpaca?](#why-alpaca)
2. [Account Setup](#account-setup)
3. [Getting API Keys](#getting-api-keys)
4. [Configuration](#configuration)
5. [Testing Connection](#testing-connection)
6. [Paper Trading vs Live Trading](#paper-trading-vs-live-trading)
7. [Troubleshooting](#troubleshooting)

---

## 🎯 Why Alpaca?

Alpaca is the **best platform for algorithmic trading** because:

- ✅ **Commission-free** trading
- ✅ **No minimum balance** required
- ✅ **Built for developers** with excellent API
- ✅ **Paper trading** included for free
- ✅ **Real-time market data**
- ✅ **Well-documented** Python SDK
- ✅ **Active community** and support

---

## 🚀 Account Setup

### Step 1: Create an Alpaca Account

1. Visit [https://alpaca.markets](https://alpaca.markets)
2. Click **"Sign Up"**
3. Choose **"Individual Account"** (for personal trading)
4. Fill in your information:
   - Email address
   - Password
   - Personal details
   - Employment information
   - Financial information

### Step 2: Verify Your Identity

1. Alpaca will ask for identity verification
2. Provide required documents:
   - Government-issued ID (driver's license, passport)
   - Social Security Number (US residents)
   - Proof of address (if required)
3. Wait for approval (usually 1-2 business days)

### Step 3: Fund Your Account (Optional for Paper Trading)

- **Paper Trading**: No funding required! You get $100,000 virtual money
- **Live Trading**: Fund via bank transfer (ACH) or wire transfer

---

## 🔑 Getting API Keys

### For Paper Trading (Recommended to Start)

1. Log in to [https://app.alpaca.markets](https://app.alpaca.markets)
2. Click on **"Paper Trading"** in the left sidebar
3. Navigate to **"Your API Keys"** section
4. Click **"Generate New Key"**
5. Give it a name (e.g., "AI Trading Bot")
6. **IMPORTANT**: Copy both keys immediately:
   - **API Key ID** (starts with `PK...`)
   - **Secret Key** (starts with `...` - only shown once!)
7. Store them securely - you'll need them for configuration

### For Live Trading (After Testing)

⚠️ **WARNING**: Only use live trading after thorough testing in paper mode!

1. Switch to **"Live Trading"** in the dashboard
2. Navigate to **"Your API Keys"**
3. Click **"Generate New Key"**
4. Copy both keys:
   - **API Key ID** (starts with `AK...`)
   - **Secret Key** (only shown once!)

---

## ⚙️ Configuration

### Step 1: Copy Environment Template

```bash
cp .env.example .env
```

### Step 2: Edit `.env` File

Open `.env` in your text editor and fill in your credentials:

```env
# Alpaca API Credentials
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Trading Mode (CRITICAL!)
ENABLE_PAPER_TRADING=True

# Safety Limits
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE_PERCENT=15.0
MAX_DAILY_LOSS_PERCENT=5.0
MIN_ACCOUNT_BALANCE=1000.0
```

### Step 3: Verify Configuration

Your `.env` file should look like this:

```env
# ✅ CORRECT - Paper Trading
ALPACA_API_KEY=PKA1B2C3D4E5F6G7H8I9
ALPACA_SECRET_KEY=abcdefghijklmnopqrstuvwxyz1234567890ABCD
ENABLE_PAPER_TRADING=True

# ❌ WRONG - Missing keys
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

---

## 🧪 Testing Connection

### Step 1: Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
python api_server.py
```

You should see:

```
============================================================
🤖 AI Trading Bot API Server Starting (Alpaca)
============================================================
INFO     Starting API server on port 5000
INFO     Trading Platform: Alpaca Markets
INFO     Paper Trading Mode: True
INFO     Debug Mode: False
============================================================
```

### Step 3: Test Authentication

1. Open [`index.html`](index.html) in your browser
2. Click **"Start Simulation"**
3. Check the console for connection status

**Expected Output:**
```
✅ Successfully authenticated with Alpaca
Account value: $100,000.00
Buying power: $100,000.00
Paper Trading: True
```

---

## 📊 Paper Trading vs Live Trading

### Paper Trading (Recommended)

**What is it?**
- Simulated trading with **virtual money** ($100,000)
- Uses **real market data** and prices
- Orders are **simulated** (not executed on real market)
- Perfect for **testing and learning**

**Configuration:**
```env
ENABLE_PAPER_TRADING=True
ALPACA_API_KEY=PK...  # Paper trading key
```

**Pros:**
- ✅ No risk of losing real money
- ✅ Test strategies safely
- ✅ Learn how the system works
- ✅ Unlimited testing

**Cons:**
- ⚠️ No real profits
- ⚠️ Simulated fills (may differ from live)

### Live Trading (Advanced)

**What is it?**
- **Real trading** with real money
- Orders executed on **actual stock market**
- **Real profits and losses**

**Configuration:**
```env
ENABLE_PAPER_TRADING=False
ALPACA_API_KEY=AK...  # Live trading key
```

**⚠️ CRITICAL WARNINGS:**

1. **Test thoroughly** in paper trading first (minimum 1-2 weeks)
2. **Start small** - use minimal amounts
3. **Monitor closely** - watch your bot constantly at first
4. **Understand risks** - you can lose money
5. **Check regulations** - Pattern Day Trading rules apply
6. **Set strict limits** - Use circuit breaker settings

---

## 🔧 Troubleshooting

### Error: "Authentication failed"

**Possible causes:**
1. Wrong API keys
2. Using live keys with paper trading mode (or vice versa)
3. Keys expired or revoked

**Solution:**
```bash
# Check your .env file
cat .env | grep ALPACA

# Verify keys match your Alpaca dashboard
# Paper keys start with PK...
# Live keys start with AK...

# Regenerate keys if needed
```

### Error: "Could not fetch price for SYMBOL"

**Possible causes:**
1. Invalid stock symbol
2. Market is closed
3. Stock is not tradeable on Alpaca

**Solution:**
```bash
# Check market status
curl http://localhost:5000/api/market/status

# Verify symbol exists
# Alpaca supports US stocks only (no OTC, penny stocks)
```

### Error: "Trade blocked by circuit breaker"

**Possible causes:**
1. Exceeded daily trade limit
2. Position size too large
3. Daily loss limit reached
4. Insufficient buying power

**Solution:**
```bash
# Check circuit breaker status
curl http://localhost:5000/api/circuit-breaker/status

# Adjust limits in .env file
MAX_DAILY_TRADES=100
MAX_POSITION_SIZE_PERCENT=20.0

# Reset circuit breaker
curl -X POST http://localhost:5000/api/circuit-breaker/reset
```

### Error: "Module not found: alpaca_trade_api"

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep alpaca
```

### Paper Trading Shows $0 Balance

**Possible causes:**
1. Using live API keys instead of paper keys
2. Paper account not initialized

**Solution:**
1. Log in to [https://app.alpaca.markets/paper/dashboard](https://app.alpaca.markets/paper/dashboard)
2. Verify paper account is active
3. Check you're using **paper trading API keys** (start with `PK...`)
4. Regenerate paper trading keys if needed

---

## 📚 Additional Resources

### Official Documentation
- [Alpaca API Docs](https://alpaca.markets/docs/)
- [Python SDK](https://github.com/alpacahq/alpaca-trade-api-python)
- [API Reference](https://alpaca.markets/docs/api-references/trading-api/)

### Alpaca Dashboard Links
- [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard/overview)
- [Live Trading Dashboard](https://app.alpaca.markets/live/dashboard/overview)
- [API Keys Management](https://app.alpaca.markets/paper/dashboard/overview)

### Support
- [Alpaca Community Slack](https://alpaca.markets/community)
- [Alpaca Support](https://alpaca.markets/support)
- [GitHub Issues](https://github.com/alpacahq/alpaca-trade-api-python/issues)

---

## ✅ Quick Checklist

Before you start trading, make sure:

- [ ] Alpaca account created and verified
- [ ] Paper trading API keys generated
- [ ] `.env` file configured with correct keys
- [ ] `ENABLE_PAPER_TRADING=True` is set
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors
- [ ] Successfully authenticated in browser
- [ ] Can see account balance ($100,000 for paper)
- [ ] Circuit breaker is active
- [ ] Tested a few manual trades
- [ ] Reviewed safety limits in `.env`

---

## 🎓 Next Steps

1. ✅ Complete this setup guide
2. 📖 Read the [QUICKSTART.md](QUICKSTART.md) guide
3. 🧪 Test in paper trading for 1-2 weeks
4. 📊 Monitor performance and adjust strategies
5. 🔧 Fine-tune safety limits
6. 💰 Consider live trading (only after thorough testing!)

---

**Remember**: Always start with paper trading. Never risk more than you can afford to lose!

🦙 **Happy Trading with Alpaca!**
