@echo off
REM ============================================================================
REM Alpaca Trading Bot - Master Launcher (Windows)
REM Double-click this file to launch everything at once
REM ============================================================================

echo ========================================================================
echo    ALPACA TRADING BOT - MASTER LAUNCHER
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
echo Checking dependencies...
pip install -q -r requirements.txt 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting all components...
echo.

REM Run the master launcher
python LAUNCH_ALL.py

pause
