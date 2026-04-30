@echo off
REM ============================================================================
REM Alpaca Trading Bot - Windows Launcher
REM Double-click this file to start the trading application
REM ============================================================================

echo ========================================================================
echo    ALPACA TRADING BOT - STARTING...
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and configure your API keys
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "venv\" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the application
echo Starting trading application...
echo.
python run_trading_app.py

pause
