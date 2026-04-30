#!/usr/bin/env python3
"""
Real-Time Portfolio Monitor
Shows live portfolio value, positions, and profit/loss updates
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from colorama import init, Fore, Back, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Load environment variables
load_dotenv()

# Configuration
ALPACA_API_KEY = os.getenv('ALPACA_API_KEY')
ALPACA_SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
ENABLE_PAPER_TRADING = os.getenv('ENABLE_PAPER_TRADING', 'True').lower() == 'true'
BASE_URL = 'https://paper-api.alpaca.markets' if ENABLE_PAPER_TRADING else 'https://api.alpaca.markets'
REFRESH_INTERVAL = 5  # seconds

# Initialize API
api = tradeapi.REST(
    key_id=ALPACA_API_KEY,
    secret_key=ALPACA_SECRET_KEY,
    base_url=BASE_URL,
    api_version='v2'
)

# Track initial values
initial_portfolio_value = None
session_start_time = datetime.now()

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_currency(value):
    """Format currency with color"""
    if value >= 0:
        return f"{Fore.GREEN}${value:,.2f}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}${value:,.2f}{Style.RESET_ALL}"

def format_percent(value):
    """Format percentage with color"""
    if value >= 0:
        return f"{Fore.GREEN}+{value:.2f}%{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{value:.2f}%{Style.RESET_ALL}"

def get_account_data():
    """Fetch account data from Alpaca"""
    try:
        account = api.get_account()
        positions = api.list_positions()
        clock = api.get_clock()
        
        return {
            'account': account,
            'positions': positions,
            'clock': clock,
            'error': None
        }
    except Exception as e:
        return {
            'account': None,
            'positions': [],
            'clock': None,
            'error': str(e)
        }

def display_dashboard(data):
    """Display the portfolio dashboard"""
    global initial_portfolio_value
    
    clear_screen()
    
    # Header
    print(f"{Back.BLUE}{Fore.WHITE}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'  📊 REAL-TIME PORTFOLIO MONITOR':^80}{Style.RESET_ALL}")
    print(f"{Back.BLUE}{Fore.WHITE}{'=' * 80}{Style.RESET_ALL}")
    
    if data['error']:
        print(f"\n{Fore.RED}❌ ERROR: {data['error']}{Style.RESET_ALL}")
        return
    
    account = data['account']
    positions = data['positions']
    clock = data['clock']
    
    # Set initial portfolio value on first run
    if initial_portfolio_value is None:
        initial_portfolio_value = float(account.portfolio_value)
    
    # Calculate metrics
    portfolio_value = float(account.portfolio_value)
    buying_power = float(account.buying_power)
    cash = float(account.cash)
    equity = float(account.equity)
    
    session_pnl = portfolio_value - initial_portfolio_value
    session_pnl_percent = (session_pnl / initial_portfolio_value * 100) if initial_portfolio_value > 0 else 0
    
    # Time info
    current_time = datetime.now()
    session_duration = current_time - session_start_time
    hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Account Summary
    print(f"\n{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}📈 ACCOUNT SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    
    print(f"\n  {'Portfolio Value:':<25} {format_currency(portfolio_value)}")
    print(f"  {'Cash:':<25} {format_currency(cash)}")
    print(f"  {'Buying Power:':<25} {format_currency(buying_power)}")
    print(f"  {'Equity:':<25} {format_currency(equity)}")
    
    # Session Performance
    print(f"\n{Fore.YELLOW}{'─' * 80}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💰 SESSION PERFORMANCE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 80}{Style.RESET_ALL}")
    
    print(f"\n  {'Starting Value:':<25} {format_currency(initial_portfolio_value)}")
    print(f"  {'Current Value:':<25} {format_currency(portfolio_value)}")
    print(f"  {'Session P&L:':<25} {format_currency(session_pnl)} ({format_percent(session_pnl_percent)})")
    print(f"  {'Session Duration:':<25} {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    # Market Status
    market_status = f"{Fore.GREEN}OPEN{Style.RESET_ALL}" if clock.is_open else f"{Fore.RED}CLOSED{Style.RESET_ALL}"
    print(f"\n{Fore.MAGENTA}{'─' * 80}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}🕐 MARKET STATUS{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'─' * 80}{Style.RESET_ALL}")
    
    print(f"\n  {'Status:':<25} {market_status}")
    print(f"  {'Current Time:':<25} {clock.timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    if not clock.is_open:
        print(f"  {'Next Open:':<25} {clock.next_open.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    else:
        print(f"  {'Next Close:':<25} {clock.next_close.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    # Positions
    print(f"\n{Fore.GREEN}{'─' * 80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 POSITIONS ({len(positions)} active){Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'─' * 80}{Style.RESET_ALL}")
    
    if positions:
        print(f"\n  {'Symbol':<8} {'Qty':<8} {'Avg Price':<12} {'Current':<12} {'Value':<14} {'P&L':<14} {'P&L %':<10}")
        print(f"  {'-' * 78}")
        
        total_position_value = 0
        total_pnl = 0
        
        for pos in positions:
            symbol = pos.symbol
            qty = float(pos.qty)
            avg_price = float(pos.avg_entry_price)
            current_price = float(pos.current_price)
            market_value = float(pos.market_value)
            unrealized_pl = float(pos.unrealized_pl)
            unrealized_plpc = float(pos.unrealized_plpc) * 100
            
            total_position_value += market_value
            total_pnl += unrealized_pl
            
            pnl_color = Fore.GREEN if unrealized_pl >= 0 else Fore.RED
            
            print(f"  {symbol:<8} {qty:<8.2f} ${avg_price:<11.2f} ${current_price:<11.2f} "
                  f"${market_value:<13,.2f} {pnl_color}${unrealized_pl:<13,.2f} "
                  f"{unrealized_plpc:>+7.2f}%{Style.RESET_ALL}")
        
        print(f"  {'-' * 78}")
        print(f"  {'TOTAL':<8} {'':<8} {'':<12} {'':<12} ${total_position_value:<13,.2f} "
              f"{format_currency(total_pnl):<22} {format_percent(total_pnl / total_position_value * 100 if total_position_value > 0 else 0)}")
    else:
        print(f"\n  {Fore.YELLOW}No open positions{Style.RESET_ALL}")
    
    # Trading Mode
    mode = f"{Fore.CYAN}📝 PAPER TRADING{Style.RESET_ALL}" if ENABLE_PAPER_TRADING else f"{Fore.RED}💰 LIVE TRADING{Style.RESET_ALL}"
    print(f"\n{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    print(f"  Mode: {mode}")
    print(f"  Dashboard: {Fore.BLUE}https://app.alpaca.markets/{'paper' if ENABLE_PAPER_TRADING else 'live'}/dashboard/overview{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    
    # Footer
    print(f"\n{Fore.WHITE}Last Updated: {current_time.strftime('%Y-%m-%d %H:%M:%S')} | "
          f"Refresh: {REFRESH_INTERVAL}s | Press Ctrl+C to exit{Style.RESET_ALL}")

def main():
    """Main monitoring loop"""
    print(f"{Fore.GREEN}🚀 Starting Real-Time Portfolio Monitor...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⏳ Connecting to Alpaca...{Style.RESET_ALL}")
    time.sleep(2)
    
    try:
        while True:
            data = get_account_data()
            display_dashboard(data)
            time.sleep(REFRESH_INTERVAL)
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}👋 Portfolio Monitor Stopped{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'=' * 80}{Style.RESET_ALL}")
        
        # Final summary
        if initial_portfolio_value:
            try:
                account = api.get_account()
                final_value = float(account.portfolio_value)
                final_pnl = final_value - initial_portfolio_value
                final_pnl_percent = (final_pnl / initial_portfolio_value * 100) if initial_portfolio_value > 0 else 0
                
                print(f"\n{Fore.CYAN}📊 Session Summary:{Style.RESET_ALL}")
                print(f"  Starting Value: {format_currency(initial_portfolio_value)}")
                print(f"  Ending Value:   {format_currency(final_value)}")
                print(f"  Total P&L:      {format_currency(final_pnl)} ({format_percent(final_pnl_percent)})")
                
                session_duration = datetime.now() - session_start_time
                hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                print(f"  Duration:       {hours:02d}:{minutes:02d}:{seconds:02d}")
            except:
                pass
        
        print(f"\n{Fore.GREEN}✅ Thank you for using Portfolio Monitor!{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()
