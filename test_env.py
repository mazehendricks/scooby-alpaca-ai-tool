"""
Test script to verify .env configuration and Alpaca API connectivity
"""

import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

# Load environment variables
load_dotenv()

print("=" * 60)
print("TESTING .ENV CONFIGURATION")
print("=" * 60)

# Check if environment variables are loaded
api_key = os.getenv('ALPACA_API_KEY')
secret_key = os.getenv('ALPACA_SECRET_KEY')
paper_trading = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'

print("\n1. Environment Variables Check:")
print(f"   ✓ ALPACA_API_KEY: {'Found' if api_key else 'Missing'} ({api_key[:10]}... if found)")
print(f"   ✓ ALPACA_SECRET_KEY: {'Found' if secret_key else 'Missing'} ({secret_key[:10]}... if found)")
print(f"   ✓ ENABLE_PAPER_TRADING: {paper_trading}")

# Determine base URL
base_url = 'https://paper-api.alpaca.markets' if paper_trading else 'https://api.alpaca.markets'
print(f"\n2. API Endpoint:")
print(f"   ✓ Base URL: {base_url}")
print(f"   ✓ Full endpoint: {base_url}/v2")

# Test API connection
print("\n3. Testing API Connection...")
try:
    api = tradeapi.REST(
        key_id=api_key,
        secret_key=secret_key,
        base_url=base_url,
        api_version='v2'
    )
    
    # Fetch account information
    account = api.get_account()
    
    print("   ✅ CONNECTION SUCCESSFUL!")
    print(f"\n4. Account Information:")
    print(f"   • Account Status: {account.status}")
    print(f"   • Portfolio Value: ${float(account.portfolio_value):,.2f}")
    print(f"   • Buying Power: ${float(account.buying_power):,.2f}")
    print(f"   • Cash: ${float(account.cash):,.2f}")
    print(f"   • Account Blocked: {account.account_blocked}")
    print(f"   • Trading Blocked: {account.trading_blocked}")
    print(f"   • Pattern Day Trader: {account.pattern_day_trader}")
    
    # Test market clock
    clock = api.get_clock()
    print(f"\n5. Market Status:")
    print(f"   • Market Open: {clock.is_open}")
    print(f"   • Current Time: {clock.timestamp}")
    print(f"   • Next Open: {clock.next_open}")
    print(f"   • Next Close: {clock.next_close}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - YOUR .ENV FILE IS WORKING CORRECTLY!")
    print("=" * 60)
    
except Exception as e:
    print(f"   ❌ CONNECTION FAILED!")
    print(f"\n   Error: {str(e)}")
    print("\n" + "=" * 60)
    print("❌ TEST FAILED - CHECK YOUR API CREDENTIALS")
    print("=" * 60)
    print("\nPossible issues:")
    print("1. Invalid API keys")
    print("2. API keys are for live trading but ENABLE_PAPER_TRADING=True")
    print("3. API keys are for paper trading but ENABLE_PAPER_TRADING=False")
    print("4. Network connectivity issues")
    print("5. Alpaca API service is down")
