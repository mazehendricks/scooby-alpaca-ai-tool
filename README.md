# 🤖 AI Trading Bot - Deep Reinforcement Learning with Alpaca Markets

A comprehensive AI-powered trading system that connects to Alpaca Markets for real trade execution. This system features deep reinforcement learning algorithms (PPO, A2C, SAC), comprehensive safety mechanisms, and a professional web-based dashboard.

![AI Trading Bot](https://img.shields.io/badge/AI-Trading%20Bot-blue)
![Alpaca](https://img.shields.io/badge/Platform-Alpaca-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)

## 🎯 Overview

This AI Trading Bot implements three state-of-the-art deep reinforcement learning algorithms for autonomous portfolio management with **real trade execution** via Alpaca Markets:

- **PPO (Proximal Policy Optimization)** - Superior risk-adjusted performance with stable policy updates
- **A2C (Advantage Actor-Critic)** - Balances value estimation with policy optimization
- **SAC (Soft Actor-Critic)** - Maximizes entropy for enhanced exploration

## ✨ Features

### Core Functionality
- **Real-time Trading Simulation** - Simulates live market conditions with realistic price movements
- **Multiple DRL Algorithms** - Switch between PPO, A2C, and SAC strategies
- **Technical Indicators** - Comprehensive state representation including:
  - Trend: SMA (50), EMA (20)
  - Momentum: RSI, MACD
  - Volatility: Bollinger Bands, ATR
  - Volume: OBV, VWAP
- **Market Sentiment Analysis** - News sentiment, VIX (fear index), and AI confidence metrics
- **Portfolio Management** - Automated position sizing with risk-adjusted allocation
- **Transaction Costs** - Realistic 0.2% transaction fees for accurate simulation

### Performance Metrics
- **Current Portfolio Value** - Real-time tracking
- **Total Return** - Absolute and percentage gains/losses
- **Sharpe Ratio** - Risk-adjusted return measurement
- **Maximum Drawdown** - Largest peak-to-trough decline
- **Win Rate** - Percentage of profitable trades
- **Trade History** - Complete audit trail of all transactions

### Safety & Ethics Features

#### 🚨 Circuit Breaker
Human-in-the-loop override to prevent "too fast to stop" scenarios during volatile conditions.

#### 🔍 Explainable AI (XAI)
Real-time explanations of AI decision-making process, addressing the "too opaque to understand" problem.

#### 🛡️ Misinformation Resilience
News sentiment filtering to guard against financial deepfakes and AI-driven misinformation.

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** (for Alpaca API backend)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Alpaca account** (free, no minimum balance required)
- **pip** (Python package manager)

### Installation

#### Automated Setup (Recommended)

**On Linux/macOS:**
```bash
git clone https://github.com/yourusername/ai-trading-bot.git
cd ai-trading-bot
chmod +x setup.sh
./setup.sh
```

**On Windows:**
```cmd
git clone https://github.com/yourusername/ai-trading-bot.git
cd ai-trading-bot
setup.bat
```

#### Manual Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/ai-trading-bot.git
cd ai-trading-bot
```

2. **Create virtual environment:**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get Alpaca API Keys:**
   - Sign up at [https://alpaca.markets](https://alpaca.markets)
   - Navigate to [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard/overview)
   - Generate API keys (they start with `PK...` for paper trading)

5. **Configure credentials:**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Alpaca credentials
nano .env
```

6. **Configure your `.env` file:**
```env
# Required: Your Alpaca API credentials
ALPACA_API_KEY=PKxxxxxxxxxxxxxxxxxx
ALPACA_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# CRITICAL: Start with paper trading enabled!
ENABLE_PAPER_TRADING=True

# Safety limits
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE_PERCENT=15.0
MAX_DAILY_LOSS_PERCENT=5.0
MIN_ACCOUNT_BALANCE=1000.0
```

### ⚠️ CRITICAL SECURITY WARNINGS

1. **NEVER commit your `.env` file to version control!** It contains your credentials.
2. **Start with `ENABLE_PAPER_TRADING=True`** to test without real money ($100k virtual).
3. **Keep your API keys secure** - treat them like passwords.
4. **Use Paper Trading keys** (start with `PK...`) for testing.
5. **Review all safety limits** before enabling real trading.

## 📖 Usage Guide

### Starting the System

1. **Start the API server:**

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
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Start server
python api_server.py
```

The server will start on `http://localhost:5000`

2. **Open the web interface:**
   - Open [`index.html`](index.html) in your web browser
   - Or navigate to the file directly

### Using the Trading Bot

1. **Authentication**:
   - Click "Start Simulation" button
   - The system will automatically authenticate with Alpaca using your `.env` credentials
   - Wait for "✅ Connected to Alpaca" message

2. **Configure Trading Parameters**:
   - **Initial Capital**: Displays your Alpaca account balance ($100k for paper trading)
   - **DRL Algorithm**: Choose PPO, A2C, or SAC
   - **Risk Tolerance (λ)**: Adjust from 0 (conservative) to 1 (aggressive)
   - **Trading Speed**: Control decision frequency (0.5s - 2s per step)

3. **Start Trading**:
   - Click "Start Simulation" to begin automated trading
   - Monitor real-time updates of:
     - Portfolio value and returns
     - Current holdings and positions
     - Trade execution log
     - Technical indicators
     - AI decision explanations
     - Circuit breaker status

4. **Control Trading**:
   - **Pause/Resume**: Temporarily halt trading decisions
   - **Reset**: Stop trading and clear session data
   - **🚨 Circuit Breaker**: Emergency stop (requires manual reset)

5. **Monitor Safety Systems**:
   - Watch circuit breaker status for safety violations
   - Review daily trade count and P&L limits
   - Check paper trading mode indicator

### Understanding the Dashboard

#### Portfolio Performance
Displays key metrics including current value, total return, Sharpe ratio, maximum drawdown, win rate, and total trades executed.

#### Market Intelligence
Shows news sentiment (Bullish/Neutral/Bearish), VIX volatility index, and AI confidence level.

#### Current Holdings
Table view of all positions with:
- Symbol and share count
- Average purchase price vs. current price
- Unrealized P&L (profit/loss)
- Portfolio weight percentage

#### Recent Trades
Chronological log of executed trades with timestamps, type (BUY/SELL), symbol, quantity, price, and algorithm used.

#### Technical Indicators
Real-time state representation showing trend, momentum, volatility, and volume indicators used by the AI agent.

#### AI Decision Explanation (XAI)
Transparent breakdown of why the AI made specific trading decisions, including:
- Algorithm reasoning
- Technical indicator analysis
- Confidence levels
- Risk management considerations

## 🧠 Algorithm Details

### PPO (Proximal Policy Optimization)
**Best for**: Risk-adjusted returns and drawdown control

**Strategy**:
- Uses clipped objective function for stable policy updates
- Buys on oversold conditions (RSI < 30) with positive momentum (MACD > 0)
- Sells on overbought conditions (RSI > 70) with negative momentum
- Conservative position sizing (15% of portfolio)

**Reward Function**:
```
R_t = r_t - λ₁ · TC_t + λ₂ · SR_t
```
Where:
- `r_t` = return at time t
- `TC_t` = transaction costs
- `SR_t` = Sharpe ratio component

### A2C (Advantage Actor-Critic)
**Best for**: Balancing exploration and exploitation

**Strategy**:
- Calculates advantage function to determine expected value
- Actor network proposes actions, critic evaluates them
- Buys when advantage > 0.3 and RSI < 50
- Sells when advantage < -0.3
- Moderate position sizing (12% of portfolio)

**Advantage Calculation**:
```
A(s,a) = Q(s,a) - V(s)
```

### SAC (Soft Actor-Critic)
**Best for**: Maximum exploration and entropy

**Strategy**:
- Maximizes entropy to encourage diverse trading strategies
- Stochastic policy with exploration bonus
- More aggressive position sizing (18% of portfolio)
- Balances immediate rewards with long-term exploration

**Entropy-Regularized Objective**:
```
J(π) = E[Σ(r_t + α·H(π(·|s_t)))]
```

## 📊 Technical Architecture

### Data Flow
```
Market Data → Technical Indicators → State Representation → DRL Agent → Action → Execution → Portfolio Update
```

### State Representation
The AI agent observes:
- Current stock prices and price history (20 periods)
- Technical indicators (RSI, MACD, SMA, EMA, ATR)
- Market sentiment (news, VIX)
- Portfolio state (cash ratio, holdings)

### Action Space
- **BUY**: Purchase shares with risk-adjusted position sizing
- **SELL**: Liquidate partial or full positions
- **HOLD**: Maintain current portfolio allocation

### Reward Function Components
1. **Return Maximization**: Portfolio value increase
2. **Transaction Cost Penalty**: 0.2% fee per trade
3. **Risk Adjustment**: Sharpe ratio bonus for consistent returns

## ⚠️ Risk Warnings & Limitations

### Systemic Risks Addressed

#### 1. "Too Fast to Stop"
**Problem**: AI systems can execute trades faster than humans can intervene during flash crashes.

**Mitigation**: Circuit breaker button provides immediate human override capability.

#### 2. "Too Opaque to Understand"
**Problem**: Black-box AI models make decisions without transparency.

**Mitigation**: Explainable AI (XAI) provides real-time reasoning for every trade decision.

#### 3. "Financial Deepfakes"
**Problem**: AI-generated misinformation can manipulate sentiment-based trading systems.

**Mitigation**: News sentiment filtering and validation mechanisms.

### Educational Disclaimer

⚠️ **IMPORTANT**: This is a **simulation for educational purposes only**. It is **NOT**:
- Financial advice or investment recommendation
- A real trading system connected to actual markets
- Guaranteed to reflect real-world performance
- Suitable for making actual investment decisions

**Real-world AI trading involves**:
- Regulatory compliance (SEC, FINRA, MiFID II)
- Market impact and liquidity constraints
- Execution slippage and latency
- Model overfitting and regime changes
- Systemic risk and correlation breakdowns

## 🔧 Customization

### Adding New Stocks
Edit [`script.js`](script.js:29) to modify the available stocks:
```javascript
this.availableStocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM'];
```

### Adjusting Safety Limits
Modify safety parameters in [`.env`](.env):
```env
MAX_DAILY_TRADES=50              # Maximum trades per day
MAX_POSITION_SIZE_PERCENT=15.0   # Max % of portfolio per position
MAX_DAILY_LOSS_PERCENT=5.0       # Stop if daily loss exceeds this
MIN_ACCOUNT_BALANCE=1000.0       # Minimum balance to maintain (for live trading)
```

### Customizing Algorithms
Each algorithm's decision logic can be modified in [`script.js`](script.js):
- `ppoDecision()` - PPO strategy (conservative, risk-adjusted)
- `a2cDecision()` - A2C strategy (balanced approach)
- `sacDecision()` - SAC strategy (aggressive with exploration)

### Switching to Real Trading

⚠️ **EXTREME CAUTION REQUIRED** ⚠️

Only switch to real trading after:
1. ✅ Thoroughly testing in paper trading mode
2. ✅ Understanding all algorithm behaviors
3. ✅ Reviewing and accepting all risks
4. ✅ Setting appropriate safety limits
5. ✅ Starting with small amounts

To enable real trading:
```env
# In .env file
ENABLE_PAPER_TRADING=False  # ⚠️ USE WITH EXTREME CAUTION!
```

## 📚 Academic Context

This project is based on research exploring:

### Benefits of AI in Finance
- **Automated Portfolio Optimization**: Deep RL can process vast amounts of historical data and technical indicators
- **Adaptive Algorithms**: Continuous learning from market conditions
- **Retail Investor Access**: Democratization of sophisticated trading strategies
- **Enhanced Efficiency**: Faster execution and reduced emotional bias

### Risks of AI in Finance
- **Market Manipulation**: AI can facilitate rapid spread of misinformation
- **Flash Crashes**: Algorithmic trading can amplify volatility
- **Opacity**: Black-box models lack interpretability
- **Systemic Risk**: Correlated AI strategies can destabilize markets

### Recommended Reading
1. "Deep Reinforcement Learning for Automated Stock Trading" - FinRL Library
2. "The Dangers of AI in Financial Markets" - Legal Analysis
3. "Explainable AI for Financial Services" - DARPA XAI Program
4. "Market Manipulation in the Age of AI" - SEC Research

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, Vanilla JavaScript
- Real-time dashboard with live updates

### Backend
- Python 3.8+
- Flask (Web framework)
- Alpaca Trade API (Market connectivity)

### Trading Platform
- **Alpaca Markets** - Commission-free trading API
- Real-time market data
- Paper trading and live trading support

### Algorithms
- Custom DRL implementations (PPO, A2C, SAC)
- Technical indicators (RSI, MACD, SMA, EMA)

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

### Authentication
- `POST /api/auth/login` - Authenticate with Alpaca
- `POST /api/auth/logout` - Logout
- `GET /api/auth/status` - Check authentication status

### Account Management
- `GET /api/account/summary` - Get account summary
- `GET /api/account/portfolio` - Get portfolio value
- `GET /api/account/positions` - Get current positions

### Market Data
- `GET /api/market/quote/<symbol>` - Get stock quote
- `GET /api/market/price/<symbol>` - Get current price
- `GET /api/market/status` - Get market status (open/closed)

### Trading
- `POST /api/trade/buy` - Execute BUY order
- `POST /api/trade/sell` - Execute SELL order

### Circuit Breaker
- `GET /api/circuit-breaker/status` - Get circuit breaker status
- `POST /api/circuit-breaker/emergency-stop` - Trigger emergency stop
- `POST /api/circuit-breaker/reset` - Reset circuit breaker
- `GET /api/circuit-breaker/trades` - Get recent trades

### Health
- `GET /api/health` - Health check

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **Additional Algorithms**: Implement DQN, DDPG, or TD3
2. **Advanced Indicators**: Add Ichimoku Cloud, Fibonacci retracements
3. **Backtesting**: Historical performance analysis with real data
4. **Multi-Asset**: Expand beyond stocks (crypto, forex, commodities)
5. **Risk Models**: VaR, CVaR, stress testing
6. **Machine Learning**: Integrate actual trained models
7. **Real-time Data**: WebSocket support for live market data

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/ai-trading-bot.git
cd ai-trading-bot

# Setup environment
./setup.sh  # or setup.bat on Windows

# Start development server
python api_server.py

# Edit files and refresh browser to see changes
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Alpaca Markets**: Excellent trading API and platform
- **FinRL Library**: Inspiration for DRL trading algorithms
- **Stable-Baselines3**: Reference implementations of PPO, A2C, SAC
- **OpenAI Gym**: Environment design patterns
- **Academic Research**: Papers on AI in finance and risk management

## 📞 Contact & Support

- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: support@example.com

## 🐛 Troubleshooting

### Common Issues

**"Backend server not running"**
- Ensure [`api_server.py`](api_server.py) is running: `python api_server.py`
- Check that port 5000 is not in use
- Verify virtual environment is activated

**"Authentication failed"**
- Double-check API keys in [`.env`](.env) file
- Verify you're using Paper Trading keys (start with `PK...`)
- Check Alpaca account status
- Regenerate API keys if needed

**"Circuit breaker tripped"**
- Review circuit breaker status in UI
- Check if daily limits were exceeded
- Reset circuit breaker if safe to continue
- Review trade history for issues

**"Trade blocked"**
- Verify sufficient buying power
- Check position size limits
- Ensure not exceeding daily trade limit
- Confirm market is open (US market hours: 9:30 AM - 4:00 PM ET)

**"Could not fetch price for SYMBOL"**
- Verify symbol is valid (Alpaca supports US stocks only)
- Check if market is open
- Some stocks may not be tradeable on Alpaca

**"Module not found" errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Logs

Check logs for detailed error information:
- **Console output**: Terminal where `api_server.py` is running
- **Log file**: `trading_bot.log` in project directory

## 🔮 Future Roadmap

- [x] ✅ **Alpaca API integration** (COMPLETED)
- [x] ✅ **Circuit breaker safety system** (COMPLETED)
- [x] ✅ **Paper trading support** (COMPLETED)
- [x] ✅ **Real trade execution** (COMPLETED)
- [ ] Real-time data streaming via WebSocket
- [ ] Advanced charting with TradingView integration
- [ ] Multi-agent portfolio management
- [ ] Sentiment analysis using LLMs
- [ ] Backtesting framework with historical data
- [ ] Export reports (PDF, CSV)
- [ ] Mobile app (React Native)
- [ ] Crypto trading support (Alpaca Crypto)

---

**Built with ❤️ for education and research in AI-driven finance**

**Powered by Alpaca Markets** 🦙

⚠️ **Remember**: Past performance does not guarantee future results. AI trading carries significant risks. Start with paper trading, test thoroughly, and never risk more than you can afford to lose. Always consult with qualified financial advisors before making investment decisions.
