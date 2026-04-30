"""
Flask API Server for Alpaca Trading Bot
Provides REST API endpoints for the frontend to interact with Alpaca Markets
"""

import logging
import colorlog
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from config import Config
from alpaca_client import alpaca_client
from circuit_breaker import circuit_breaker

# Configure logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(getattr(logging, Config.LOG_LEVEL))

# Also log to file
file_handler = logging.FileHandler(Config.LOG_FILE)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(file_handler)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
CORS(app)  # Enable CORS for frontend communication

logger.info("=" * 60)
logger.info("🤖 AI Trading Bot API Server Starting (Alpaca)")
logger.info("=" * 60)


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate with Alpaca"""
    try:
        success, message = alpaca_client.login()
        
        if success:
            account_summary = alpaca_client.get_account_summary()
            return jsonify({
                'success': True,
                'message': message,
                'account': account_summary
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 401
            
    except Exception as e:
        logger.error(f"Login endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Server error: {str(e)}"
        }), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout from Alpaca"""
    try:
        alpaca_client.logout()
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        logger.error(f"Logout endpoint error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    return jsonify({
        'authenticated': alpaca_client.authenticated,
        'paper_trading': Config.ENABLE_PAPER_TRADING
    }), 200


# ============================================================================
# ACCOUNT ENDPOINTS
# ============================================================================

@app.route('/api/account/summary', methods=['GET'])
def account_summary():
    """Get account summary"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        summary = alpaca_client.get_account_summary()
        return jsonify(summary), 200
    except Exception as e:
        logger.error(f"Account summary error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/account/portfolio', methods=['GET'])
def portfolio_value():
    """Get portfolio value"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        value = alpaca_client.get_portfolio_value()
        buying_power = alpaca_client.get_buying_power()
        
        return jsonify({
            'portfolio_value': value,
            'buying_power': buying_power,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Portfolio value error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/account/positions', methods=['GET'])
def positions():
    """Get current positions"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        positions = alpaca_client.get_positions()
        return jsonify({
            'positions': positions,
            'count': len(positions)
        }), 200
    except Exception as e:
        logger.error(f"Positions error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# MARKET DATA ENDPOINTS
# ============================================================================

@app.route('/api/market/quote/<symbol>', methods=['GET'])
def get_quote(symbol):
    """Get stock quote"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        quote = alpaca_client.get_stock_quote(symbol.upper())
        if quote:
            return jsonify(quote), 200
        else:
            return jsonify({'error': f'Could not fetch quote for {symbol}'}), 404
    except Exception as e:
        logger.error(f"Quote error for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/market/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """Get current stock price"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        price = alpaca_client.get_stock_price(symbol.upper())
        return jsonify({
            'symbol': symbol.upper(),
            'price': price,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Price error for {symbol}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/market/status', methods=['GET'])
def market_status():
    """Get market status (open/closed)"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        status = alpaca_client.get_market_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Market status error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# TRADING ENDPOINTS
# ============================================================================

@app.route('/api/trade/buy', methods=['POST'])
def execute_buy():
    """Execute a BUY order"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        quantity = float(data.get('quantity', 0))
        
        if not symbol or quantity <= 0:
            return jsonify({'error': 'Invalid symbol or quantity'}), 400
        
        success, message, order_details = alpaca_client.execute_buy(symbol, quantity)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'order': order_details,
                'circuit_breaker': circuit_breaker.get_status()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
            
    except Exception as e:
        logger.error(f"Buy order error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/trade/sell', methods=['POST'])
def execute_sell():
    """Execute a SELL order"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        quantity = float(data.get('quantity', 0))
        
        if not symbol or quantity <= 0:
            return jsonify({'error': 'Invalid symbol or quantity'}), 400
        
        success, message, order_details = alpaca_client.execute_sell(symbol, quantity)
        
        if success:
            return jsonify({
                'success': True,
                'message': message,
                'order': order_details,
                'circuit_breaker': circuit_breaker.get_status()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 400
            
    except Exception as e:
        logger.error(f"Sell order error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


# ============================================================================
# CIRCUIT BREAKER ENDPOINTS
# ============================================================================

@app.route('/api/circuit-breaker/status', methods=['GET'])
def circuit_breaker_status():
    """Get circuit breaker status"""
    try:
        status = circuit_breaker.get_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Circuit breaker status error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/circuit-breaker/emergency-stop', methods=['POST'])
def emergency_stop():
    """Trigger emergency stop"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'Manual emergency stop from frontend')
        
        circuit_breaker.emergency_stop(reason)
        
        return jsonify({
            'success': True,
            'message': 'Emergency stop activated',
            'status': circuit_breaker.get_status()
        }), 200
    except Exception as e:
        logger.error(f"Emergency stop error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/circuit-breaker/reset', methods=['POST'])
def reset_circuit_breaker():
    """Reset circuit breaker"""
    try:
        success = circuit_breaker.reset()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Circuit breaker reset',
                'status': circuit_breaker.get_status()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Cannot reset - manual intervention required'
            }), 400
    except Exception as e:
        logger.error(f"Circuit breaker reset error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/circuit-breaker/trades', methods=['GET'])
def recent_trades():
    """Get recent trades"""
    try:
        limit = request.args.get('limit', 10, type=int)
        trades = circuit_breaker.get_recent_trades(limit)
        
        return jsonify({
            'trades': trades,
            'count': len(trades)
        }), 200
    except Exception as e:
        logger.error(f"Recent trades error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# LIVE METRICS ENDPOINTS
# ============================================================================

@app.route('/api/metrics/live', methods=['GET'])
def live_metrics():
    """Get live portfolio metrics including performance stats"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        account = alpaca_client.api.get_account()
        positions = alpaca_client.get_positions()
        cb_status = circuit_breaker.get_status()
        
        # Calculate metrics
        portfolio_value = float(account.portfolio_value)
        equity = float(account.equity)
        cash = float(account.cash)
        buying_power = float(account.buying_power)
        
        # Calculate total P&L
        total_pnl = sum(pos['pnl'] for pos in positions)
        total_pnl_percent = (total_pnl / portfolio_value * 100) if portfolio_value > 0 else 0
        
        # Calculate win rate from recent trades
        trades = circuit_breaker.get_recent_trades(100)
        winning_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
        win_rate = (winning_trades / len(trades) * 100) if trades else 0
        
        # Calculate max drawdown (simplified)
        starting_balance = cb_status.get('starting_balance', portfolio_value)
        max_drawdown = ((portfolio_value - starting_balance) / starting_balance * 100) if starting_balance > 0 else 0
        
        # Calculate Sharpe ratio (simplified daily estimate)
        daily_return = cb_status.get('daily_pnl', 0) / starting_balance if starting_balance > 0 else 0
        sharpe_ratio = daily_return * (252 ** 0.5) if daily_return != 0 else 0  # Annualized
        
        return jsonify({
            'portfolio_value': portfolio_value,
            'equity': equity,
            'cash': cash,
            'buying_power': buying_power,
            'total_return': total_pnl,
            'total_return_percent': total_pnl_percent,
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_drawdown': round(max_drawdown, 2),
            'win_rate': round(win_rate, 2),
            'total_trades': len(trades),
            'positions_count': len(positions),
            'daily_pnl': cb_status.get('daily_pnl', 0),
            'daily_trades': cb_status.get('daily_trades_count', 0),
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Live metrics error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/performance', methods=['GET'])
def performance_metrics():
    """Get detailed performance metrics"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        account = alpaca_client.api.get_account()
        positions = alpaca_client.get_positions()
        
        portfolio_value = float(account.portfolio_value)
        
        # Position analysis
        position_values = [pos['current_value'] for pos in positions]
        total_position_value = sum(position_values)
        
        # Concentration risk
        largest_position = max(position_values) if position_values else 0
        concentration_risk = (largest_position / portfolio_value * 100) if portfolio_value > 0 else 0
        
        # Diversification
        diversification_score = len(positions) * 10  # Simple score
        
        return jsonify({
            'portfolio_value': portfolio_value,
            'positions_count': len(positions),
            'total_position_value': total_position_value,
            'cash_percent': (float(account.cash) / portfolio_value * 100) if portfolio_value > 0 else 0,
            'concentration_risk': round(concentration_risk, 2),
            'diversification_score': min(diversification_score, 100),
            'positions': positions,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Performance metrics error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# RISK MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/risk/limits', methods=['GET'])
def get_risk_limits():
    """Get current risk management limits"""
    try:
        limits = circuit_breaker.config
        status = circuit_breaker.get_status()
        
        return jsonify({
            'limits': limits,
            'current_status': status,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Get risk limits error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/risk/limits', methods=['POST'])
def update_risk_limits():
    """Update risk management limits"""
    try:
        data = request.get_json()
        
        # Update circuit breaker configuration
        if 'max_daily_trades' in data:
            circuit_breaker.config['max_daily_trades'] = int(data['max_daily_trades'])
        
        if 'max_daily_loss_percent' in data:
            circuit_breaker.config['max_daily_loss_percent'] = float(data['max_daily_loss_percent'])
        
        if 'max_position_size_percent' in data:
            circuit_breaker.config['max_position_size_percent'] = float(data['max_position_size_percent'])
        
        if 'min_account_balance' in data:
            circuit_breaker.config['min_account_balance'] = float(data['min_account_balance'])
        
        logger.info(f"Risk limits updated: {circuit_breaker.config}")
        
        return jsonify({
            'success': True,
            'message': 'Risk limits updated',
            'limits': circuit_breaker.config
        }), 200
    except Exception as e:
        logger.error(f"Update risk limits error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/risk/stop-loss', methods=['POST'])
def set_stop_loss():
    """Set stop-loss for a position"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        stop_price = float(data.get('stop_price', 0))
        
        if not symbol or stop_price <= 0:
            return jsonify({'error': 'Invalid symbol or stop price'}), 400
        
        # Get current position
        positions = alpaca_client.get_positions()
        position = next((p for p in positions if p['symbol'] == symbol), None)
        
        if not position:
            return jsonify({'error': f'No position found for {symbol}'}), 404
        
        # Create stop-loss order
        order = alpaca_client.api.submit_order(
            symbol=symbol,
            qty=position['quantity'],
            side='sell',
            type='stop',
            stop_price=stop_price,
            time_in_force='gtc'
        )
        
        logger.info(f"Stop-loss set for {symbol} at ${stop_price}")
        
        return jsonify({
            'success': True,
            'message': f'Stop-loss set for {symbol}',
            'order_id': order.id,
            'stop_price': stop_price
        }), 200
    except Exception as e:
        logger.error(f"Stop-loss error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/risk/take-profit', methods=['POST'])
def set_take_profit():
    """Set take-profit for a position"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').upper()
        limit_price = float(data.get('limit_price', 0))
        
        if not symbol or limit_price <= 0:
            return jsonify({'error': 'Invalid symbol or limit price'}), 400
        
        # Get current position
        positions = alpaca_client.get_positions()
        position = next((p for p in positions if p['symbol'] == symbol), None)
        
        if not position:
            return jsonify({'error': f'No position found for {symbol}'}), 404
        
        # Create take-profit order
        order = alpaca_client.api.submit_order(
            symbol=symbol,
            qty=position['quantity'],
            side='sell',
            type='limit',
            limit_price=limit_price,
            time_in_force='gtc'
        )
        
        logger.info(f"Take-profit set for {symbol} at ${limit_price}")
        
        return jsonify({
            'success': True,
            'message': f'Take-profit set for {symbol}',
            'order_id': order.id,
            'limit_price': limit_price
        }), 200
    except Exception as e:
        logger.error(f"Take-profit error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


@app.route('/api/risk/close-all', methods=['POST'])
def close_all_positions():
    """Close all open positions (emergency liquidation)"""
    if not alpaca_client.authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Close all positions
        alpaca_client.api.close_all_positions()
        
        logger.warning("🚨 All positions closed (emergency liquidation)")
        
        return jsonify({
            'success': True,
            'message': 'All positions closed'
        }), 200
    except Exception as e:
        logger.error(f"Close all positions error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error: {str(e)}"
        }), 500


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'authenticated': alpaca_client.authenticated,
        'paper_trading': Config.ENABLE_PAPER_TRADING,
        'circuit_breaker_active': circuit_breaker.state.is_active,
        'platform': 'Alpaca Markets'
    }), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'name': 'AI Trading Bot API (Alpaca)',
        'version': '2.0.0',
        'platform': 'Alpaca Markets',
        'status': 'running',
        'endpoints': {
            'auth': ['/api/auth/login', '/api/auth/logout', '/api/auth/status'],
            'account': ['/api/account/summary', '/api/account/portfolio', '/api/account/positions'],
            'market': ['/api/market/quote/<symbol>', '/api/market/price/<symbol>', '/api/market/status'],
            'trading': ['/api/trade/buy', '/api/trade/sell'],
            'circuit_breaker': [
                '/api/circuit-breaker/status',
                '/api/circuit-breaker/emergency-stop',
                '/api/circuit-breaker/reset',
                '/api/circuit-breaker/trades'
            ],
            'health': ['/api/health']
        }
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info(f"Starting API server on port {Config.PORT}")
    logger.info(f"Trading Platform: Alpaca Markets")
    logger.info(f"Paper Trading Mode: {Config.ENABLE_PAPER_TRADING}")
    logger.info(f"Debug Mode: {Config.DEBUG}")
    logger.info("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=Config.PORT,
        debug=Config.DEBUG
    )
