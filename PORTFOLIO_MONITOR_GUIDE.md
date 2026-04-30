# 📊 Real-Time Portfolio Monitor Guide

## 🎯 What You're Seeing

The portfolio monitor is now running and shows:

### 📈 Account Summary
- **Portfolio Value** - Total value of your account
- **Cash** - Available cash balance
- **Buying Power** - Amount you can use to buy stocks (includes margin)
- **Equity** - Value of your stock positions

### 💰 Session Performance
- **Starting Value** - Portfolio value when you started the monitor
- **Current Value** - Real-time portfolio value
- **Session P&L** - Profit/Loss since you started monitoring
- **Session Duration** - How long the monitor has been running

### 🕐 Market Status
- **Status** - Whether market is OPEN or CLOSED
- **Current Time** - Current market time
- **Next Open/Close** - When market opens/closes next

### 📊 Positions
Shows all your active stock positions with:
- Symbol
- Quantity (shares owned)
- Average Price (what you paid)
- Current Price (real-time price)
- Market Value (current worth)
- P&L (profit/loss in dollars)
- P&L % (profit/loss percentage)

## 🎨 Color Coding

- 🟢 **Green** - Positive values (profit)
- 🔴 **Red** - Negative values (loss)
- 🔵 **Blue** - Headers and info
- 🟡 **Yellow** - Warnings and session info
- 🟣 **Purple** - Market status
- 🔷 **Cyan** - Account summary

## 🔄 Auto-Refresh

The monitor updates every **5 seconds** automatically, so you see:
- Real-time price changes
- Live P&L updates
- Position value changes
- Portfolio value fluctuations

## 🚀 How to Use

### Start the Monitor
```bash
python3 portfolio_monitor.py
```

### Stop the Monitor
Press `Ctrl+C` to stop and see a final session summary

### Run in Background
```bash
python3 portfolio_monitor.py &
```

## 📱 What Happens When You Trade

1. **Execute a trade** using `execute_trade.py` or the web interface
2. **Watch the monitor** - it will show:
   - New position appears in the positions list
   - Portfolio value changes
   - P&L updates in real-time
   - Cash balance decreases (for buys) or increases (for sells)

## 💡 Example Workflow

### Terminal 1: Run Portfolio Monitor
```bash
python3 portfolio_monitor.py
```

### Terminal 2: Execute Trades
```bash
python3 execute_trade.py
# Buy 10 shares of AAPL
```

### Terminal 1: Watch Changes
- Position appears immediately
- P&L updates every 5 seconds
- See profit/loss in real-time

## 📊 Understanding the Display

### Current Display Shows:
```
Portfolio Value: $100,000.00  ← Your total account value
Cash: $100,000.00             ← Available cash (no positions yet)
Buying Power: $200,000.00     ← Can buy up to this amount (2x margin)
Session P&L: $0.00 (+0.00%)   ← No profit/loss yet (no trades)
```

### After Buying 10 AAPL @ $150:
```
Portfolio Value: $100,000.00  ← Still same (just moved cash to stock)
Cash: $98,500.00              ← Reduced by $1,500 (10 × $150)
Positions:
  AAPL    10.00   $150.00   $151.00   $1,510.00   +$10.00   +0.67%
                   ↑         ↑         ↑           ↑         ↑
                   Bought at Current   Worth now   Profit    Profit %
```

### If AAPL Goes Up to $155:
```
Portfolio Value: $100,050.00  ← Increased by $50
Session P&L: +$50.00 (+0.05%) ← Your profit!
Positions:
  AAPL    10.00   $150.00   $155.00   $1,550.00   +$50.00   +3.33%
```

## 🎯 Key Features

✅ **Real-time updates** every 5 seconds
✅ **Color-coded** profit/loss
✅ **Session tracking** - see total profit since start
✅ **Multiple positions** - tracks all your stocks
✅ **Market status** - know when you can trade
✅ **Clean display** - easy to read
✅ **Session summary** - final report when you exit

## ⚠️ Important Notes

- **Market Closed**: Prices won't change when market is closed
- **Paper Trading**: This is practice money, not real
- **5-Second Delay**: Updates every 5 seconds (not instant)
- **Terminal Required**: Must keep terminal open to see updates

## 🔧 Customization

Edit `portfolio_monitor.py` to change:

```python
REFRESH_INTERVAL = 5  # Change to 1 for faster updates (1 second)
                      # Change to 10 for slower updates (10 seconds)
```

## 📈 Best Practices

1. **Keep it running** while trading to see real-time changes
2. **Use with execute_trade.py** for manual trading
3. **Watch during market hours** for live price action
4. **Check session P&L** to track your performance
5. **Press Ctrl+C** to see final summary before closing

## 🎉 You're All Set!

Your portfolio monitor is running and will show:
- ✅ Real-time portfolio value
- ✅ Live profit/loss updates
- ✅ All position changes
- ✅ Session performance tracking

Execute some trades and watch your portfolio change in real-time!
