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
