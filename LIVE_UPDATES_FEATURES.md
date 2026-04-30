# Live Updates & Risk Management Features

## 🎯 Overview
This document describes the new live portfolio metrics, real-time updates, and advanced risk management features added to the Alpaca AI Trading System.

## ✨ New Features Implemented

### 1. Live Portfolio Metrics API Endpoints

#### `/api/metrics/live` (GET)
Returns real-time portfolio performance metrics:
- **Portfolio Value**: Current total portfolio value
- **Total Return**: Absolute and percentage returns
- **Sharpe Ratio**: Risk-adjusted return metric
- **Max Drawdown**: Peak-to-trough decline percentage
- **Win Rate**: Percentage of profitable trades
- **Total Trades**: Number of executed trades
- **Daily P&L**: Profit/loss for current trading day
- **Positions Count**: Number of open positions

**Response Example:**
```json
{
  "portfolio_value": 10500.00,
  "equity": 10500.00,
  "cash": 5000.00,
  "buying_power": 20000.00,
  "total_return": 500.00,
  "total_return_percent": 5.00,
  "sharpe_ratio": 1.25,
  "max_drawdown": -2.50,
  "win_rate": 65.00,
  "total_trades": 25,
  "positions_count": 5,
  "daily_pnl": 150.00,
  "daily_trades": 8,
  "timestamp": "2026-04-30T04:00:00Z"
}
```

#### `/api/metrics/performance` (GET)
Returns detailed performance analysis:
- Position concentration risk
- Diversification score
- Cash allocation percentage
- Individual position details

### 2. Advanced Risk Management Endpoints

#### `/api/risk/limits` (GET/POST)
**GET**: Retrieve current risk management limits
**POST**: Update risk limits dynamically

**Configurable Limits:**
- `max_daily_trades`: Maximum trades per day (default: 50)
- `max_daily_loss_percent`: Maximum daily loss percentage (default: 5%)
- `max_position_size_percent`: Maximum single position size (default: 20%)
- `min_account_balance`: Minimum account balance threshold (default: $1000)

**Update Example:**
```json
{
  "max_daily_trades": 100,
  "max_daily_loss_percent": 3.0,
  "max_position_size_percent": 15.0,
  "min_account_balance": 2000.00
}
```

#### `/api/risk/stop-loss` (POST)
Set stop-loss orders for positions to limit downside risk.

**Request:**
```json
{
  "symbol": "AAPL",
  "stop_price": 150.00
}
```

**Features:**
- Automatically creates stop-loss order for existing position
- Validates position exists before creating order
- Uses GTC (Good 'Til Cancelled) time in force

#### `/api/risk/take-profit` (POST)
Set take-profit orders to lock in gains.

**Request:**
```json
{
  "symbol": "AAPL",
  "limit_price": 200.00
}
```

#### `/api/risk/close-all` (POST)
Emergency liquidation - closes all open positions immediately.

**Use Cases:**
- Market crash scenarios
- Emergency risk reduction
- End of trading session cleanup

### 3. Real-Time Updates System

#### Polling Mechanism
- **Update Frequency**: Every 2 seconds
- **Auto-start**: Begins on page load
- **Continuous**: Runs independently of trading state

#### Live Updated Metrics
All portfolio metrics update automatically:
- ✅ Portfolio Value (live)
- ✅ Total Return (live)
- ✅ Sharpe Ratio (live)
- ✅ Max Drawdown (live)
- ✅ Win Rate (live)
- ✅ Total Trades (live)

#### Implementation Details
```javascript
// Starts automatically on page load
startLiveUpdates();

// Updates every 2 seconds
setInterval(async () => {
    await updateLiveMetrics();
}, 2000);
```

### 4. Enhanced UI Controls

#### Risk Management Control Panel
New section with 4 control cards:

**📊 Position Limits**
- Max Daily Trades input
- Max Position Size (%) input
- Update button to apply changes

**💰 Loss Protection**
- Max Daily Loss (%) input
- Min Account Balance ($) input
- Update button to apply changes

**🎯 Position Management**
- Symbol input
- Stop-Loss Price input
- Set Stop-Loss button

**💎 Take-Profit Orders**
- Symbol input
- Take-Profit Price input
- Set Take-Profit button

**🚨 Emergency Controls**
- Large "CLOSE ALL POSITIONS" button
- Warning message about immediate liquidation
- Confirmation dialog before execution

### 5. Enhanced Button Functionality

#### All Buttons Now Live-Updated:
- **START TRADING**: Initiates live updates and trading loop
- **PAUSE TRADING**: Maintains live updates while pausing trades
- **RESET**: Clears data and resets circuit breaker
- **EMERGENCY STOP**: Triggers circuit breaker and halts all activity

#### Button States:
- Disabled when not applicable
- Visual feedback on hover
- Clear status indicators

### 6. Holdings Table Auto-Update
The positions table now updates automatically:
- Refreshes with each trading cycle
- Shows real-time P&L
- Displays current prices
- Calculates portfolio weight

## 🔧 Technical Implementation

### Backend Changes (api_server.py)
- Added 7 new API endpoints
- Integrated with circuit breaker system
- Real-time metrics calculation
- Position management functions

### Frontend Changes (script.js)
- Live update polling system
- Risk management functions
- UI handler functions
- Global function exposure for onclick handlers

### Styling (style.css)
- Risk controls section styling
- Button variants (small, danger-large)
- Control group styling
- Emergency controls styling
- Hover effects and transitions

## 📊 Usage Examples

### Setting Risk Limits
1. Navigate to "Advanced Risk Management Controls"
2. Adjust sliders/inputs for desired limits
3. Click "Update Limits" button
4. Confirmation appears in trade log

### Setting Stop-Loss
1. Enter symbol (e.g., "AAPL")
2. Enter stop-loss price (e.g., 150.00)
3. Click "Set Stop-Loss"
4. Order created and logged

### Monitoring Live Metrics
- All metrics update automatically every 2 seconds
- No manual refresh needed
- Works whether trading is active or paused

### Emergency Liquidation
1. Click "CLOSE ALL POSITIONS" button
2. Confirm action in dialog
3. All positions closed at market price
4. Confirmation in trade log

## 🛡️ Safety Features

### Circuit Breaker Integration
All risk management features integrate with the circuit breaker:
- Trades blocked if limits exceeded
- Automatic trip on threshold breach
- Manual emergency stop capability
- Reset functionality with validation

### Validation
- Input validation on all forms
- Position existence checks
- Price validation (must be > 0)
- Symbol format validation (uppercase)

### User Feedback
- Real-time trade log updates
- Success/error messages
- Visual indicators (colors, icons)
- Confirmation dialogs for destructive actions

## 🚀 Performance

### Optimizations
- Efficient polling (2-second intervals)
- Minimal API calls
- Cached state management
- Conditional updates

### Resource Usage
- Low bandwidth (small JSON payloads)
- Minimal CPU usage
- No memory leaks
- Clean interval management

## 📝 Configuration

### Default Settings
```javascript
riskLimits: {
    maxDailyTrades: 50,
    maxDailyLossPercent: 5,
    maxPositionSizePercent: 20,
    minAccountBalance: 1000
}
```

### Customization
All limits can be adjusted via the UI or by modifying the initial state in `script.js`.

## 🔍 Monitoring

### What's Live
- ✅ Portfolio Value
- ✅ Total Return & %
- ✅ Sharpe Ratio
- ✅ Max Drawdown
- ✅ Win Rate
- ✅ Total Trades
- ✅ Positions Table
- ✅ Daily P&L
- ✅ Circuit Breaker Status

### What's Simulated
- Technical Indicators (SMA, EMA, RSI, etc.)
- Market Sentiment
- AI Confidence
- Trade decisions (when not authenticated)

## 🎓 Best Practices

1. **Set Stop-Losses**: Always protect positions with stop-loss orders
2. **Monitor Limits**: Keep an eye on daily trade and loss limits
3. **Use Take-Profits**: Lock in gains with take-profit orders
4. **Emergency Stop**: Don't hesitate to use emergency stop if needed
5. **Review Metrics**: Check live metrics regularly for performance insights

## 🐛 Troubleshooting

### Live Updates Not Working
- Check browser console for errors
- Verify API server is running
- Ensure authentication is successful
- Check network tab for API calls

### Risk Limits Not Applying
- Verify inputs are valid numbers
- Check trade log for error messages
- Ensure circuit breaker is not tripped
- Try resetting the system

### Positions Not Updating
- Confirm authentication status
- Check if positions exist in Alpaca account
- Verify API connectivity
- Review server logs for errors

## 📚 API Reference Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/metrics/live` | GET | Real-time portfolio metrics |
| `/api/metrics/performance` | GET | Detailed performance analysis |
| `/api/risk/limits` | GET | Get current risk limits |
| `/api/risk/limits` | POST | Update risk limits |
| `/api/risk/stop-loss` | POST | Set stop-loss order |
| `/api/risk/take-profit` | POST | Set take-profit order |
| `/api/risk/close-all` | POST | Close all positions |

## 🎉 Summary

The system now features:
- **Live Updates**: All key metrics update every 2 seconds
- **Risk Management**: Comprehensive tools to control trading risk
- **Position Protection**: Stop-loss and take-profit orders
- **Emergency Controls**: Quick liquidation capability
- **Enhanced UI**: Intuitive controls for all features
- **Real-time Feedback**: Immediate confirmation of all actions

All features are production-ready and fully integrated with the Alpaca Markets API and circuit breaker system.
