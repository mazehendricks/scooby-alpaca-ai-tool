#!/usr/bin/env python3
"""
Manual Trade Execution Script
Execute a single trade without simulation
"""

import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from datetime import datetime

# Load environment variables
load_dotenv()

# Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ENABLE_PAPER_TRADING = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'
BASE_URL = 'https://paper-api.alpaca.markets' if ENABLE_PAPER_TRADING else 'https://api.alpaca.markets'

print("=" * 70)
print("🎯 MANUAL TRADE EXECUTION")
print("=" * 70)

# Initialize API
api = tradeapi.REST(
    key_id=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    base_url=BASE_URL,
    api_version='v2'
)

# Check account
account = api.get_account()
print(f"\n📊 Account Status:")
print(f"   • Portfolio Value: ${float(account.portfolio_value):,.2f}")
print(f"   • Buying Power: ${float(account.buying_power):,.2f}")
print(f"   • Cash: ${float(account.cash):,.2f}")
print(f"   • Paper Trading: {ENABLE_PAPER_TRADING}")

# Check market status
clock = api.get_clock()
print(f"\n🕐 Market Status:")
print(f"   • Market Open: {clock.is_open}")
print(f"   • Current Time: {clock.timestamp}")

if not clock.is_open:
    print(f"   • Next Open: {clock.next_open}")
    print(f"\n⚠️  WARNING: Market is currently CLOSED")
    print(f"   Orders will be queued and executed when market opens")

# Get user input for trade
print("\n" + "=" * 70)
print("TRADE DETAILS")
print("=" * 70)

symbol = input("\nEnter stock symbol (e.g., AAPL, TSLA, SPY): ").upper().strip()
if not symbol:
    print("❌ No symbol entered. Exiting.")
    exit(1)

# Get current price
try:
    trade = api.get_latest_trade(symbol)
    current_price = float(trade.price)
    print(f"\n💰 Current Price of {symbol}: ${current_price:.2f}")
except Exception as e:
    print(f"❌ Could not fetch price for {symbol}: {str(e)}")
    exit(1)

# Get quantity
try:
    quantity = int(input(f"\nEnter quantity (number of shares): ").strip())
    if quantity <= 0:
        print("❌ Quantity must be positive")
        exit(1)
except ValueError:
    print("❌ Invalid quantity")
    exit(1)

# Get action
action = input("\nEnter action (BUY or SELL): ").upper().strip()
if action not in ['BUY', 'SELL']:
    print("❌ Invalid action. Must be BUY or SELL")
    exit(1)

# Calculate total cost
total_cost = quantity * current_price
print(f"\n📋 Order Summary:")
print(f"   • Symbol: {symbol}")
print(f"   • Action: {action}")
print(f"   • Quantity: {quantity} shares")
print(f"   • Price: ${current_price:.2f}")
print(f"   • Total Value: ${total_cost:,.2f}")

# Confirm
confirm = input(f"\n⚠️  Confirm {action} {quantity} shares of {symbol}? (yes/no): ").lower().strip()
if confirm not in ['yes', 'y']:
    print("❌ Trade cancelled")
    exit(0)

# Execute trade
print(f"\n🚀 Executing {action} order...")
try:
    order = api.submit_order(
        symbol=symbol,
        qty=quantity,
        side=action.lower(),
        type='market',
        time_in_force='gtc'  # Good 'til cancelled
    )
    
    print("\n" + "=" * 70)
    print("✅ ORDER EXECUTED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\n📄 Order Details:")
    print(f"   • Order ID: {order.id}")
    print(f"   • Symbol: {order.symbol}")
    print(f"   • Side: {order.side.upper()}")
    print(f"   • Quantity: {order.qty}")
    print(f"   • Type: {order.type}")
    print(f"   • Status: {order.status}")
    print(f"   • Submitted At: {order.submitted_at}")
    
    if ENABLE_PAPER_TRADING:
        print(f"\n📝 This was a PAPER TRADING order (no real money)")
        print(f"   View in dashboard: https://app.alpaca.markets/paper/dashboard/overview")
    else:
        print(f"\n💰 This was a LIVE TRADING order (REAL MONEY)")
        print(f"   View in dashboard: https://app.alpaca.markets/live/dashboard/overview")
    
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"\n❌ ORDER FAILED: {str(e)}")
    print("\nPossible reasons:")
    print("1. Insufficient buying power")
    print("2. Invalid symbol")
    print("3. Market is closed (order will be queued)")
    print("4. Position doesn't exist (for SELL orders)")
    exit(1)
