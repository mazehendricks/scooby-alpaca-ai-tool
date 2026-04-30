"""
Alpaca API Client
Handles authentication and trading operations with Alpaca Markets
"""

import logging
import alpaca_trade_api as tradeapi
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import Config
from circuit_breaker import circuit_breaker

logger = logging.getLogger(__name__)


class AlpacaClient:
    """
    Alpaca API Client with safety features
    
    Provides secure authentication and trade execution with
    circuit breaker integration for Alpaca Markets
    """
    
    def __init__(self):
        self.authenticated = False
        self.api = None
        self.account_info = None
        self.positions = {}
        logger.info("Alpaca Client initialized")
    
    def login(self) -> Tuple[bool, str]:
        """
        Authenticate with Alpaca
        
        Returns:
            (success: bool, message: str)
        """
        try:
            # Validate configuration
            Config.validate()
            
            # Determine base URL (paper or live trading)
            base_url = Config.ALPACA_BASE_URL
            
            # Initialize Alpaca API
            logger.info(f"Attempting connection to Alpaca ({base_url})")
            
            self.api = tradeapi.REST(
                key_id=Config.ALPACA_API_KEY,
                secret_key=Config.ALPACA_SECRET_KEY,
                base_url=base_url,
                api_version='v2'
            )
            
            # Test connection by fetching account
            account = self.api.get_account()
            
            if account:
                self.authenticated = True
                self.account_info = account
                
                # Activate circuit breaker with current balance
                portfolio_value = float(account.portfolio_value)
                circuit_breaker.activate(portfolio_value)
                
                logger.info("✅ Successfully authenticated with Alpaca")
                logger.info(f"Account value: ${portfolio_value:,.2f}")
                logger.info(f"Buying power: ${float(account.buying_power):,.2f}")
                logger.info(f"Paper Trading: {Config.ENABLE_PAPER_TRADING}")
                
                return True, "Successfully authenticated"
            else:
                logger.error("❌ Authentication failed")
                return False, "Authentication failed - check credentials"
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False, f"Login error: {str(e)}"
    
    def logout(self):
        """Logout from Alpaca (close connection)"""
        try:
            self.api = None
            self.authenticated = False
            circuit_breaker.deactivate()
            logger.info("Disconnected from Alpaca")
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
    
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
    
    def get_buying_power(self) -> float:
        """Get available buying power"""
        try:
            if not self.api:
                return 0.0
            account = self.api.get_account()
            return float(account.buying_power)
        except Exception as e:
            logger.error(f"Error fetching buying power: {str(e)}")
            return 0.0
    
    def get_positions(self) -> List[Dict]:
        """Get current stock positions"""
        try:
            if not self.api:
                return []
            
            positions = self.api.list_positions()
            result = []
            
            for position in positions:
                symbol = position.symbol
                quantity = float(position.qty)
                avg_price = float(position.avg_entry_price)
                current_price = float(position.current_price)
                current_value = float(position.market_value)
                pnl = float(position.unrealized_pl)
                pnl_percent = float(position.unrealized_plpc) * 100
                
                result.append({
                    'symbol': symbol,
                    'quantity': quantity,
                    'average_price': avg_price,
                    'current_price': current_price,
                    'current_value': current_value,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent
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
            
            # Get latest trade
            trade = self.api.get_latest_trade(symbol)
            if trade:
                return float(trade.price)
            
            # Fallback to last quote
            quote = self.api.get_latest_quote(symbol)
            if quote:
                return float(quote.ask_price)
            
            return 0.0
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {str(e)}")
            return 0.0
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """Get detailed stock quote"""
        try:
            if not self.api:
                return {}
            
            quote = self.api.get_latest_quote(symbol)
            trade = self.api.get_latest_trade(symbol)
            
            if quote and trade:
                return {
                    'symbol': symbol,
                    'price': float(trade.price),
                    'ask_price': float(quote.ask_price),
                    'bid_price': float(quote.bid_price),
                    'ask_size': int(quote.ask_size),
                    'bid_size': int(quote.bid_size),
                    'timestamp': trade.timestamp.isoformat()
                }
            return {}
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {str(e)}")
            return {}
    
    def execute_buy(self, symbol: str, quantity: float, order_type: str = 'market') -> Tuple[bool, str, Optional[Dict]]:
        """
        Execute a BUY order with circuit breaker protection
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            order_type: 'market' or 'limit'
        
        Returns:
            (success: bool, message: str, order_details: Dict)
        """
        if not self.authenticated or not self.api:
            return False, "Not authenticated", None
        
        try:
            # Get current price
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            # Check with circuit breaker
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'BUY', quantity, price, portfolio_value
            )
            
            if not allowed:
                logger.warning(f"Trade blocked by circuit breaker: {reason}")
                return False, f"Trade blocked: {reason}", None
            
            # Execute order
            logger.info(f"Executing BUY order: {quantity} {symbol} @ ${price:.2f}")
            
            order = self.api.submit_order(
                symbol=symbol,
                qty=quantity,
                side='buy',
                type='market',
                time_in_force='gtc'  # Good 'til cancelled
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
                
                mode = "📝 PAPER" if Config.ENABLE_PAPER_TRADING else "💰 LIVE"
                logger.info(f"✅ {mode} BUY order executed: {quantity} {symbol} @ ${price:.2f}")
                return True, "Order executed successfully", order_details
            else:
                logger.error(f"❌ BUY order failed")
                return False, "Order failed", None
                
        except Exception as e:
            logger.error(f"Error executing BUY order: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def execute_sell(self, symbol: str, quantity: float, order_type: str = 'market') -> Tuple[bool, str, Optional[Dict]]:
        """
        Execute a SELL order with circuit breaker protection
        
        Args:
            symbol: Stock symbol
            quantity: Number of shares
            order_type: 'market' or 'limit'
        
        Returns:
            (success: bool, message: str, order_details: Dict)
        """
        if not self.authenticated or not self.api:
            return False, "Not authenticated", None
        
        try:
            # Get current price
            price = self.get_stock_price(symbol)
            if price == 0:
                return False, f"Could not fetch price for {symbol}", None
            
            # Check with circuit breaker
            portfolio_value = self.get_portfolio_value()
            allowed, reason = circuit_breaker.check_trade_allowed(
                symbol, 'SELL', quantity, price, portfolio_value
            )
            
            if not allowed:
                logger.warning(f"Trade blocked by circuit breaker: {reason}")
                return False, f"Trade blocked: {reason}", None
            
            # Execute order
            logger.info(f"Executing SELL order: {quantity} {symbol} @ ${price:.2f}")
            
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
                
                mode = "📝 PAPER" if Config.ENABLE_PAPER_TRADING else "💰 LIVE"
                logger.info(f"✅ {mode} SELL order executed: {quantity} {symbol} @ ${price:.2f}")
                return True, "Order executed successfully", order_details
            else:
                logger.error(f"❌ SELL order failed")
                return False, "Order failed", None
                
        except Exception as e:
            logger.error(f"Error executing SELL order: {str(e)}")
            return False, f"Error: {str(e)}", None
    
    def get_account_summary(self) -> Dict:
        """Get comprehensive account summary"""
        try:
            if not self.api:
                return {'error': 'Not connected'}
            
            account = self.api.get_account()
            portfolio_value = float(account.portfolio_value)
            buying_power = float(account.buying_power)
            positions = self.get_positions()
            
            total_pnl = sum(pos['pnl'] for pos in positions)
            
            return {
                'authenticated': self.authenticated,
                'portfolio_value': portfolio_value,
                'buying_power': buying_power,
                'cash': float(account.cash),
                'positions_count': len(positions),
                'positions': positions,
                'total_pnl': total_pnl,
                'account_blocked': account.account_blocked,
                'trading_blocked': account.trading_blocked,
                'pattern_day_trader': account.pattern_day_trader,
                'circuit_breaker': circuit_breaker.get_status(),
                'paper_trading': Config.ENABLE_PAPER_TRADING
            }
        except Exception as e:
            logger.error(f"Error getting account summary: {str(e)}")
            return {'error': str(e)}
    
    def get_market_status(self) -> Dict:
        """Get market clock and status"""
        try:
            if not self.api:
                return {}
            
            clock = self.api.get_clock()
            return {
                'is_open': clock.is_open,
                'timestamp': clock.timestamp.isoformat(),
                'next_open': clock.next_open.isoformat(),
                'next_close': clock.next_close.isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting market status: {str(e)}")
            return {}


# Global client instance
alpaca_client = AlpacaClient()
