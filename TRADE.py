#!/usr/bin/env python3
"""
SIMPLE ALPACA TRADING TERMINAL
Just works. No HTML. No complexity.
"""

import os
import sys
import time
from datetime import datetime
import alpaca_trade_api as tradeapi
from colorama import init, Fore, Style

init(autoreset=True)

# Your API keys (hardcoded so it actually works)
API_KEY = "PKXQF2AG2SH7DJROKJ4STNQNQZ"
SECRET_KEY = "CuDGXrrEDfLMEpu4WZYds3vEzA7Sa6ggE6KCFJFKESQD"
BASE_URL = "https://paper-api.alpaca.markets"

# Connect to Alpaca
print(f"{Fore.CYAN}{'='*70}")
print(f"{Fore.CYAN}🚀 ALPACA TRADING TERMINAL")
print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

print(f"{Fore.YELLOW}Connecting to Alpaca...{Style.RESET_ALL}")

try:
    api = tradeapi.REST(
        key_id=API_KEY,
        secret_key=SECRET_KEY,
        base_url=BASE_URL,
        api_version='v2'
    )
    account = api.get_account()
    print(f"{Fore.GREEN}✅ Connected!{Style.RESET_ALL}\n")
except Exception as e:
    print(f"{Fore.RED}❌ Connection failed: {e}{Style.RESET_ALL}")
    sys.exit(1)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_portfolio():
    """Show current portfolio"""
    try:
        account = api.get_account()
        positions = api.list_positions()
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"📊 PORTFOLIO")
        print(f"{'='*70}{Style.RESET_ALL}")
        
        portfolio_value = float(account.portfolio_value)
        cash = float(account.cash)
        buying_power = float(account.buying_power)
        
        print(f"\n{Fore.WHITE}Portfolio Value: {Fore.GREEN}${portfolio_value:,.2f}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Cash:            {Fore.GREEN}${cash:,.2f}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Buying Power:    {Fore.GREEN}${buying_power:,.2f}{Style.RESET_ALL}")
        
        if positions:
            print(f"\n{Fore.CYAN}POSITIONS:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'Symbol':<8} {'Qty':<8} {'Price':<12} {'Value':<14} {'P&L':<14} {'P&L %':<10}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{'-'*70}{Style.RESET_ALL}")
            
            total_pnl = 0
            for pos in positions:
                symbol = pos.symbol
                qty = float(pos.qty)
                current_price = float(pos.current_price)
                market_value = float(pos.market_value)
                unrealized_pl = float(pos.unrealized_pl)
                unrealized_plpc = float(pos.unrealized_plpc) * 100
                
                total_pnl += unrealized_pl
                
                pnl_color = Fore.GREEN if unrealized_pl >= 0 else Fore.RED
                
                print(f"{Fore.YELLOW}{symbol:<8}{Style.RESET_ALL} "
                      f"{qty:<8.2f} ${current_price:<11.2f} ${market_value:<13,.2f} "
                      f"{pnl_color}${unrealized_pl:<13,.2f} {unrealized_plpc:>+7.2f}%{Style.RESET_ALL}")
            
            total_color = Fore.GREEN if total_pnl >= 0 else Fore.RED
            print(f"{Fore.WHITE}{'-'*70}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}TOTAL P&L: {total_color}${total_pnl:,.2f}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}No open positions{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def get_price(symbol):
    """Get current stock price"""
    try:
        trade = api.get_latest_trade(symbol)
        return float(trade.price)
    except:
        return None

def buy_stock():
    """Buy stock"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"💰 BUY STOCK")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    symbol = input(f"{Fore.WHITE}Enter symbol (e.g., AAPL): {Style.RESET_ALL}").upper().strip()
    if not symbol:
        return
    
    # Get current price
    price = get_price(symbol)
    if not price:
        print(f"{Fore.RED}❌ Could not fetch price for {symbol}{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}Current price: ${price:.2f}{Style.RESET_ALL}")
    
    try:
        qty = int(input(f"{Fore.WHITE}Enter quantity: {Style.RESET_ALL}"))
        if qty <= 0:
            print(f"{Fore.RED}Invalid quantity{Style.RESET_ALL}")
            return
    except:
        print(f"{Fore.RED}Invalid quantity{Style.RESET_ALL}")
        return
    
    total_cost = qty * price
    print(f"\n{Fore.YELLOW}Total cost: ${total_cost:,.2f}{Style.RESET_ALL}")
    
    confirm = input(f"{Fore.WHITE}Confirm BUY {qty} {symbol}? (yes/no): {Style.RESET_ALL}").lower()
    if confirm not in ['yes', 'y']:
        print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")
        return
    
    try:
        print(f"{Fore.YELLOW}Executing order...{Style.RESET_ALL}")
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"{Fore.GREEN}✅ BUY order executed!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Order ID: {order.id}{Style.RESET_ALL}")
        time.sleep(2)
    except Exception as e:
        print(f"{Fore.RED}❌ Order failed: {e}{Style.RESET_ALL}")
        time.sleep(2)

def sell_stock():
    """Sell stock"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"💸 SELL STOCK")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # Show current positions
    positions = api.list_positions()
    if not positions:
        print(f"{Fore.YELLOW}No positions to sell{Style.RESET_ALL}")
        time.sleep(2)
        return
    
    print(f"{Fore.CYAN}Your positions:{Style.RESET_ALL}")
    for i, pos in enumerate(positions, 1):
        print(f"{i}. {pos.symbol} - {float(pos.qty)} shares @ ${float(pos.current_price):.2f}")
    
    symbol = input(f"\n{Fore.WHITE}Enter symbol to sell: {Style.RESET_ALL}").upper().strip()
    if not symbol:
        return
    
    # Check if we have this position
    position = None
    for pos in positions:
        if pos.symbol == symbol:
            position = pos
            break
    
    if not position:
        print(f"{Fore.RED}You don't own {symbol}{Style.RESET_ALL}")
        time.sleep(2)
        return
    
    max_qty = float(position.qty)
    current_price = float(position.current_price)
    
    print(f"{Fore.GREEN}You own {max_qty} shares @ ${current_price:.2f}{Style.RESET_ALL}")
    
    try:
        qty = int(input(f"{Fore.WHITE}Enter quantity to sell (max {max_qty}): {Style.RESET_ALL}"))
        if qty <= 0 or qty > max_qty:
            print(f"{Fore.RED}Invalid quantity{Style.RESET_ALL}")
            return
    except:
        print(f"{Fore.RED}Invalid quantity{Style.RESET_ALL}")
        return
    
    total_value = qty * current_price
    print(f"\n{Fore.YELLOW}Total value: ${total_value:,.2f}{Style.RESET_ALL}")
    
    confirm = input(f"{Fore.WHITE}Confirm SELL {qty} {symbol}? (yes/no): {Style.RESET_ALL}").lower()
    if confirm not in ['yes', 'y']:
        print(f"{Fore.YELLOW}Cancelled{Style.RESET_ALL}")
        return
    
    try:
        print(f"{Fore.YELLOW}Executing order...{Style.RESET_ALL}")
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print(f"{Fore.GREEN}✅ SELL order executed!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Order ID: {order.id}{Style.RESET_ALL}")
        time.sleep(2)
    except Exception as e:
        print(f"{Fore.RED}❌ Order failed: {e}{Style.RESET_ALL}")
        time.sleep(2)

def main_menu():
    """Main menu"""
    while True:
        clear_screen()
        show_portfolio()
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"MENU")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Buy Stock")
        print(f"2. Sell Stock")
        print(f"3. Refresh")
        print(f"4. Exit{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.YELLOW}Choose option: {Style.RESET_ALL}").strip()
        
        if choice == '1':
            buy_stock()
        elif choice == '2':
            sell_stock()
        elif choice == '3':
            continue
        elif choice == '4':
            print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}Invalid option{Style.RESET_ALL}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
