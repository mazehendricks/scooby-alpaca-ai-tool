@echo off
REM Quick start script for the API server (Windows)

echo 🚀 Starting AI Trading Bot API Server...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Check if .env exists
if not exist .env (
    echo ❌ Error: .env file not found!
    echo Please run setup.bat first and configure your credentials.
    pause
    exit /b 1
)

REM Start the server
python api_server.py
pause
