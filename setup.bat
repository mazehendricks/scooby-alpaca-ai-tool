@echo off
REM Setup script for AI Trading Bot with Robinhood Integration (Windows)

echo ==================================================
echo 🤖 AI Trading Bot - Setup Script (Windows)
echo ==================================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your Robinhood credentials.
) else (
    echo.
    echo ⚠️  .env file already exists. Skipping...
)

echo.
echo ==================================================
echo ✅ Setup complete!
echo ==================================================
echo.
echo Next steps:
echo 1. Edit .env file with your Robinhood credentials
echo 2. Activate virtual environment: venv\Scripts\activate
echo 3. Start the API server: python api_server.py
echo 4. Open index.html in your browser
echo.
echo ⚠️  IMPORTANT: Start with ENABLE_PAPER_TRADING=True for testing!
echo.
pause
