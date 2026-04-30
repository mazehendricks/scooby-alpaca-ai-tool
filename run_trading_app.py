#!/usr/bin/env python3
"""
Alpaca Trading Bot - All-in-One Application
Complete trading application with web interface in a single file
"""

import os
import sys
import logging
import webbrowser
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from threading import Lock
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import alpaca_trade_api as tradeapi

# ============================================================================
# CONFIGURATION
# ============================================================================

load_dotenv()

class Config:
    """Application configuration"""
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
    ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
    ENABLE_PAPER_TRADING = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'
    ALPACA_BASE_URL = os.getenv(
        'ALPACA_BASE_URL',
        'https://paper-api.alpaca.markets' if ENABLE_PAPER_TRADING else 'https://api.alpaca.markets'
    )
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    MAX_DAILY_TRADES = int(os.getenv('MAX_DAILY_TRADES', 50))
    MAX_POSITION_SIZE_PERCENT = float(os.getenv('MAX_POSITION_SIZE_PERCENT', 15.0))
    MAX_DAILY_LOSS_PERCENT = float(os.getenv('MAX_DAILY_LOSS_PERCENT', 5.0))
    MIN_ACCOUNT_BALANCE = float(os.getenv('MIN_ACCOUNT_BALANCE', 1000.0))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trading_bot.log')
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CIRCUIT BREAKER
# ============================================================================

class CircuitBreaker:
    """Safety mechanism to prevent excessive losses and overtrading"""
    
    def __init__(self):
        self.active = False
        self.initial_balance = 0.0
        self.current_balance = 0.0
        self.daily_trades = 0
        self.trade_history = []
        self.positions = {}
        self.last_reset = datetime.now().date()
        self.lock = Lock()
        self.tripped = False
        self.trip_reason = None
    
    def activate(self, initial_balance: float):
        """Activate circuit breaker with initial balance"""
        with self.lock:
            self.active = True
            self.initial_balance = initial_balance
            self.current_balance = initial_balance
            self.daily_trades = 0
            self.trade_history = []
            self.positions = {}
            self.tripped = False
            self.trip_reason = None
            logger.info(f"Circuit breaker activated with balance: ${initial_balance:,.2f}")
    
    def deactivate(self):
        """Deactivate circuit breaker"""
        with self.lock:
            self.active = False
            self.tripped = False
            logger.info("Circuit breaker deactivated")
    
    def reset_daily_counters(self):
        """Reset daily counters if new day"""
        today = datetime.now().date()
        if today > self.last_reset:
            with self.lock:
                self.daily_trades = 0
                self.trade_history = [t for t in self.trade_history 
                                     if datetime.fromisoformat(t['timestamp']).date() == today]
                self.last_reset = today
                logger.info("Daily counters reset")
    
    def check_trade_allowed(self, symbol: str, action: str, quantity: float, 
                           price: float, portfolio_value: float) -> Tuple[bool, str]:
        """Check if trade is allowed"""
        if not self.active:
            return True, "Circuit breaker not active"
        
        self.reset_daily_counters()
        
        with self.lock:
            if self.tripped:
                return False, f"Circuit breaker tripped: {self.trip_reason}"
            
            # Check daily trade limit
            if self.daily_trades >= Config.MAX_DAILY_TRADES:
                self.tripped = True
                self.trip_reason = f"Daily trade limit reached ({Config.MAX_DAILY_TRADES})"
                return False, self.trip_reason
            
            # Check daily loss limit
            daily_loss_percent = ((self.initial_balance - portfolio_value) / self.initial_balance) * 100
            if daily_loss_percent > Config.MAX_DAILY_LOSS_PERCENT:
                self.tripped = True
                self.trip_reason = f"Daily loss limit exceeded ({daily_loss_percent:.2f}%)"
                return False, self.trip_reason
            
            # Check minimum balance
            if portfolio_value < Config.MIN_ACCOUNT_BALANCE:
                self.tripped = True
                self.trip_reason = f"Account balance below minimum (${Config.MIN_ACCOUNT_BALANCE:,.2f})"
                return False, self.trip_reason
            
            # Check position size for BUY orders
            if action == 'BUY':
                position_value = quantity * price
                position_percent = (position_value / portfolio_value) * 100
                if position_percent > Config.MAX_POSITION_SIZE_PERCENT:
                    return False, f"Position size too large ({position_percent:.2f}% > {Config.MAX_POSITION_SIZE_PERCENT}%)"
            
            return True, "Trade allowed"
    
    def record_trade(self, symbol: str, action: str, quantity: float, price: float):
        """Record a trade"""
        with self.lock:
            self.daily_trades += 1
            self.trade_history.append({
                'symbol': symbol,
                'action': action,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now().isoformat()
            })
            
            if action == 'BUY':
                self.positions[symbol] = self.positions.get(symbol, 0) + quantity
            elif action == 'SELL':
                self.positions[symbol] = self.positions.get(symbol, 0) - quantity
    
    def update_balance(self, new_balance: float):
        """Update current balance"""
        with self.lock:
            self.current_balance = new_balance
    
    def get_status(self) -> Dict:
        """Get circuit breaker status"""
        with self.lock:
            return {
                'active': self.active,
                'tripped': self.tripped,
                'trip_reason': self.trip_reason,
                'daily_trades': self.daily_trades,
                'max_daily_trades': Config.MAX_DAILY_TRADES,
                'initial_balance': self.initial_balance,
                'current_balance': self.current_balance,
                'positions': self.positions
            }

circuit_breaker = CircuitBreaker()

# ============================================================================
# ALPACA CLIENT
# ============================================================================

class AlpacaClient:
    """Alpaca API Client with safety features"""
    
    def __init__(self):
        self.authenticated = False
        self.api = None
        self.account_info = None
    
    def login(self) -> Tuple[bool, str]:
        """Authenticate with Alpaca"""
        try:
            if not Config.ALPACA_API_KEY or not Config.ALPACA_SECRET_KEY:
                return False, "API credentials not configured"
            
            logger.info(f"Connecting to Alpaca ({Config.ALPACA_BASE_URL})")
            
            self.api = tradeapi.REST(
                key_id=Config.ALPACA_API_KEY,
                secret_key=Config.ALPACA_SECRET_KEY,
                base_url=Config.ALPACA_BASE_URL,
                api_version='v2'
            )
            
            account = self.api.get_account()
            
            if account:
                self.authenticated = True
                self.account_info = account
                portfolio_value = float(account.portfolio_value)
                circuit_breaker.activate(portfolio_value)
                
                logger.info(f"✅ Authenticated - Portfolio: ${portfolio_value:,.2f}")
                return True, "Successfully authenticated"
            else:
                return False, "Authentication failed"
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"Login error: {str(e)}"
    
    def logout(self):
        """Logout from Alpaca"""
        self.api = None
        self.authenticated = False
        circuit_breaker.deactivate()
        logger.info("Disconnected from Alpaca")
    
    def get_portfolio_value(self) -> float:
        """Get total portfolio value"""
        try:
            if not self.api:
                return 0.0
            account = self.api.get_account()
            return float(account.portfolio_value)
        except Exception as e:
            logger.error(f"Error fetching portfolio value: {str(e)}")
            return 0.0
    
    def get_positions(self) -> List[Dict]:
        """Get current positions"""
        try:
            if not self.api:
                return []
            
            positions = self.api.list_positions()
            result = []
            
            for position in positions:
                result.append({
                    'symbol': position.symbol,
                    'quantity': float(position.qty),
                    'average_price': float(position.avg_entry_price),
                    'current_price': float(position.current_price),
                    'current_value': float(position.market_value),
                    'pnl': float(position.unrealized_pl),
                    'pnl_percent': float(position.unrealized_plpc) * 100
                })
            
            return result
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            return []
    
    def get_stock_price(self, symbol: str) -> float:
        """Get current stock price"""
        try:
            if not self.api:
                return 0.0
            trade = self.api.get_latest_trade(symbol)
            return float(trade.price) if trade else 0.0
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {str(e)}")
            return 0.0
    
    def execute_buy(self, symbol: str, quantity: float) -> Tuple[bool, str, Optional[Dict]]:
        """Execute BUY order"""
        if not self.authenticated or not self.api:
            return False, "Not authenticated", None
        
        try:
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'BUY', quantity, price, portfolio_value
            )
            
            if not allowed:
                return False, f"Trade blocked: {reason}", None
            
            logger.info(f"Executing BUY: {quantity} {symbol} @ ${price:.2f}")
            
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            
            if order:
                circuit_breaker.record_trade(symbol, 'BUY', quantity, price)
                circuit_breaker.update_balance(self.get_portfolio_value())
                
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'order_id': order.id,
                    'status': order.status,
                    'type': 'BUY',
                    'timestamp': datetime.now().isoformat(),
                    'paper_trading': Config.ENABLE_PAPER_TRADING
                }
                
                logger.info(f"✅ BUY order executed: {quantity} {symbol}")
                return True, "Order executed successfully", order_details
            else:
                return False, "Order failed", None
                
        except Exception as e:
            logger.error(f"Error executing BUY: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def execute_sell(self, symbol: str, quantity: float) -> Tuple[bool, str, Optional[Dict]]:
        """Execute SELL order"""
        if not self.authenticated or not self.api:
            return False, "Not authenticated", None
        
        try:
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'SELL', quantity, price, portfolio_value
            )
            
            if not allowed:
                return False, f"Trade blocked: {reason}", None
            
            logger.info(f"Executing SELL: {quantity} {symbol} @ ${price:.2f}")
            
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            
            if order:
                circuit_breaker.record_trade(symbol, 'SELL', quantity, price)
                circuit_breaker.update_balance(self.get_portfolio_value())
                
                order_details = {
                    'symbol': symbol,
                    'quantity': quantity,
                    'price': price,
                    'order_id': order.id,
                    'status': order.status,
                    'type': 'SELL',
                    'timestamp': datetime.now().isoformat(),
                    'paper_trading': Config.ENABLE_PAPER_TRADING
                }
                
                logger.info(f"✅ SELL order executed: {quantity} {symbol}")
                return True, "Order executed successfully", order_details
            else:
                return False, "Order failed", None
                
        except Exception as e:
            logger.error(f"Error executing SELL: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def get_account_summary(self) -> Dict:
        """Get account summary"""
        try:
            if not self.api:
                return {'error': 'Not connected'}
            
            account = self.api.get_account()
            positions = self.get_positions()
            total_pnl = sum(pos['pnl'] for pos in positions)
            
            return {
                'authenticated': self.authenticated,
                'portfolio_value': float(account.portfolio_value),
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'positions_count': len(positions),
                'positions': positions,
                'total_pnl': total_pnl,
                'circuit_breaker': circuit_breaker.get_status(),
                'paper_trading': Config.ENABLE_PAPER_TRADING
            }
        except Exception as e:
            logger.error(f"Error getting account summary: {str(e)}")
            return {'error': str(e)}

alpaca_client = AlpacaClient()

# ============================================================================
# FLASK WEB APPLICATION
# ============================================================================

app = Flask(__name__, static_folder='.')
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/login', methods=['POST'])
def api_login():
    """Login endpoint"""
    success, message = alpaca_client.login()
    return jsonify({'success': success, 'message': message})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Logout endpoint"""
    alpaca_client.logout()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/account', methods=['GET'])
def api_account():
    """Get account summary"""
    summary = alpaca_client.get_account_summary()
    return jsonify(summary)

@app.route('/api/positions', methods=['GET'])
def api_positions():
    """Get current positions"""
    positions = alpaca_client.get_positions()
    return jsonify({'positions': positions})

@app.route('/api/price/<symbol>', methods=['GET'])
def api_price(symbol):
    """Get stock price"""
    price = alpaca_client.get_stock_price(symbol.upper())
    return jsonify({'symbol': symbol.upper(), 'price': price})

@app.route('/api/trade', methods=['POST'])
def api_trade():
    """Execute trade"""
    data = request.json
    symbol = data.get('symbol', '').upper()
    action = data.get('action', '').upper()
    quantity = float(data.get('quantity', 0))
    
    if not symbol or not action or quantity <= 0:
        return jsonify({'success': False, 'message': 'Invalid trade parameters'})
    
    if action == 'BUY':
        success, message, details = alpaca_client.execute_buy(symbol, quantity)
    elif action == 'SELL':
        success, message, details = alpaca_client.execute_sell(symbol, quantity)
    else:
        return jsonify({'success': False, 'message': 'Invalid action'})
    
    return jsonify({
        'success': success,
        'message': message,
        'order': details
    })

@app.route('/api/circuit-breaker/status', methods=['GET'])
def api_circuit_breaker_status():
    """Get circuit breaker status"""
    return jsonify(circuit_breaker.get_status())

@app.route('/api/circuit-breaker/reset', methods=['POST'])
def api_circuit_breaker_reset():
    """Reset circuit breaker"""
    if alpaca_client.authenticated:
        portfolio_value = alpaca_client.get_portfolio_value()
        circuit_breaker.activate(portfolio_value)
        return jsonify({'success': True, 'message': 'Circuit breaker reset'})
    return jsonify({'success': False, 'message': 'Not authenticated'})

@app.route('/api/health', methods=['GET'])
def api_health():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'authenticated': alpaca_client.authenticated,
        'paper_trading': Config.ENABLE_PAPER_TRADING,
        'timestamp': datetime.now().isoformat()
    })

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    print("=" * 70)
    print("🚀 ALPACA TRADING BOT - ALL-IN-ONE APPLICATION")
    print("=" * 70)
    print(f"\n📊 Configuration:")
    print(f"   • Paper Trading: {Config.ENABLE_PAPER_TRADING}")
    print(f"   • API Endpoint: {Config.ALPACA_BASE_URL}")
    print(f"   • Port: {Config.PORT}")
    print(f"   • Max Daily Trades: {Config.MAX_DAILY_TRADES}")
    print(f"   • Max Position Size: {Config.MAX_POSITION_SIZE_PERCENT}%")
    print(f"   • Max Daily Loss: {Config.MAX_DAILY_LOSS_PERCENT}%")
    print(f"\n🌐 Starting web server...")
    print(f"   • Local: http://localhost:{Config.PORT}")
    print(f"   • Network: http://127.0.0.1:{Config.PORT}")
    print(f"\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 70)
    
    # Open browser automatically
    try:
        webbrowser.open(f'http://localhost:{Config.PORT}')
    except:
        pass
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG,
        use_reloader=False
    )

if __name__ == '__main__':
    main()
