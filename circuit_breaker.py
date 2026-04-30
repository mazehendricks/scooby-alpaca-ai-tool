"""
Circuit Breaker Implementation
Provides safety mechanisms to prevent "too fast to stop" scenarios
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from config import Config

logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    """Record of a single trade"""
    timestamp: datetime
    symbol: str
    action: str  # 'BUY' or 'SELL'
    quantity: float
    price: float
    value: float


@dataclass
class CircuitBreakerState:
    """Current state of the circuit breaker"""
    is_active: bool = False
    is_tripped: bool = False
    daily_trades: List[TradeRecord] = field(default_factory=list)
    daily_pnl: float = 0.0
    starting_balance: float = 0.0
    current_balance: float = 0.0
    last_reset: datetime = field(default_factory=datetime.now)
    trip_reason: Optional[str] = None


class CircuitBreaker:
    """
    Circuit Breaker for AI Trading System
    
    Implements multiple safety mechanisms:
    1. Maximum daily trades limit
    2. Maximum daily loss percentage
    3. Minimum account balance protection
    4. Position size limits
    5. Manual emergency stop
    """
    
    def __init__(self):
        self.state = CircuitBreakerState()
        self.config = Config.get_safety_limits()
        self.manual_stop = False
        logger.info("Circuit Breaker initialized with limits: %s", self.config)
    
    def activate(self, starting_balance: float):
        """Activate the circuit breaker for a trading session"""
        self.state.is_active = True
        self.state.is_tripped = False
        self.state.starting_balance = starting_balance
        self.state.current_balance = starting_balance
        self.state.daily_trades = []
        self.state.daily_pnl = 0.0
        self.state.last_reset = datetime.now()
        self.state.trip_reason = None
        self.manual_stop = False
        logger.info(f"Circuit Breaker ACTIVATED - Starting balance: ${starting_balance:,.2f}")
    
    def deactivate(self):
        """Deactivate the circuit breaker"""
        self.state.is_active = False
        logger.info("Circuit Breaker DEACTIVATED")
    
    def emergency_stop(self, reason: str = "Manual emergency stop"):
        """Manually trip the circuit breaker"""
        self.manual_stop = True
        self.state.is_tripped = True
        self.state.trip_reason = reason
        logger.critical(f"🚨 EMERGENCY STOP ACTIVATED: {reason}")
    
    def reset(self):
        """Reset the circuit breaker (use with caution)"""
        if self.manual_stop:
            logger.warning("Cannot auto-reset after manual emergency stop. Requires manual intervention.")
            return False
        
        self.state.is_tripped = False
        self.state.trip_reason = None
        logger.info("Circuit Breaker RESET")
        return True
    
    def check_trade_allowed(self, symbol: str, action: str, quantity: float, 
                           price: float, current_portfolio_value: float) -> tuple[bool, str]:
        """
        Check if a trade is allowed based on safety limits
        
        Returns:
            (allowed: bool, reason: str)
        """
        if not self.state.is_active:
            return False, "Circuit breaker not active"
        
        if self.state.is_tripped:
            return False, f"Circuit breaker tripped: {self.state.trip_reason}"
        
        if self.manual_stop:
            return False, "Manual emergency stop is active"
        
        # Check if we need to reset daily counters (new day)
        if datetime.now().date() > self.state.last_reset.date():
            self._reset_daily_counters()
        
        # 1. Check maximum daily trades
        if len(self.state.daily_trades) >= self.config['max_daily_trades']:
            self._trip(f"Maximum daily trades reached ({self.config['max_daily_trades']})")
            return False, self.state.trip_reason
        
        # 2. Check maximum daily loss
        daily_loss_percent = (self.state.daily_pnl / self.state.starting_balance) * 100
        if daily_loss_percent < -self.config['max_daily_loss_percent']:
            self._trip(f"Maximum daily loss exceeded ({daily_loss_percent:.2f}%)")
            return False, self.state.trip_reason
        
        # 3. Check minimum account balance
        if current_portfolio_value < self.config['min_account_balance']:
            self._trip(f"Account balance below minimum (${current_portfolio_value:,.2f})")
            return False, self.state.trip_reason
        
        # 4. Check position size limit (for BUY orders)
        if action.upper() == 'BUY':
            trade_value = quantity * price
            position_percent = (trade_value / current_portfolio_value) * 100
            
            if position_percent > self.config['max_position_size_percent']:
                return False, f"Position size too large ({position_percent:.2f}% > {self.config['max_position_size_percent']}%)"
        
        # 5. Paper trading check
        if self.config['paper_trading_enabled']:
            logger.info(f"📝 PAPER TRADING MODE - Trade would be executed: {action} {quantity} {symbol} @ ${price}")
        
        return True, "Trade allowed"
    
    def record_trade(self, symbol: str, action: str, quantity: float, 
                    price: float, pnl: float = 0.0):
        """Record a completed trade"""
        trade = TradeRecord(
            timestamp=datetime.now(),
            symbol=symbol,
            action=action.upper(),
            quantity=quantity,
            price=price,
            value=quantity * price
        )
        
        self.state.daily_trades.append(trade)
        self.state.daily_pnl += pnl
        
        logger.info(f"Trade recorded: {action} {quantity} {symbol} @ ${price:.2f} | Daily P&L: ${self.state.daily_pnl:,.2f}")
    
    def update_balance(self, new_balance: float):
        """Update current account balance"""
        self.state.current_balance = new_balance
    
    def get_status(self) -> Dict:
        """Get current circuit breaker status"""
        daily_loss_percent = 0.0
        if self.state.starting_balance > 0:
            daily_loss_percent = (self.state.daily_pnl / self.state.starting_balance) * 100
        
        return {
            'active': self.state.is_active,
            'tripped': self.state.is_tripped,
            'trip_reason': self.state.trip_reason,
            'manual_stop': self.manual_stop,
            'daily_trades_count': len(self.state.daily_trades),
            'max_daily_trades': self.config['max_daily_trades'],
            'daily_pnl': self.state.daily_pnl,
            'daily_loss_percent': daily_loss_percent,
            'max_daily_loss_percent': self.config['max_daily_loss_percent'],
            'current_balance': self.state.current_balance,
            'starting_balance': self.state.starting_balance,
            'paper_trading': self.config['paper_trading_enabled'],
            'limits': self.config
        }
    
    def get_recent_trades(self, limit: int = 10) -> List[Dict]:
        """Get recent trades"""
        recent = self.state.daily_trades[-limit:]
        return [
            {
                'timestamp': trade.timestamp.isoformat(),
                'symbol': trade.symbol,
                'action': trade.action,
                'quantity': trade.quantity,
                'price': trade.price,
                'value': trade.value
            }
            for trade in recent
        ]
    
    def _trip(self, reason: str):
        """Trip the circuit breaker"""
        self.state.is_tripped = True
        self.state.trip_reason = reason
        logger.critical(f"🚨 CIRCUIT BREAKER TRIPPED: {reason}")
    
    def _reset_daily_counters(self):
        """Reset daily counters for a new trading day"""
        logger.info("New trading day - resetting daily counters")
        self.state.daily_trades = []
        self.state.daily_pnl = 0.0
        self.state.starting_balance = self.state.current_balance
        self.state.last_reset = datetime.now()


# Global circuit breaker instance
circuit_breaker = CircuitBreaker()
