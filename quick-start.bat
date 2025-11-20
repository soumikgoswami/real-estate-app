@echo off
REM Quick Start Script for Real Estate Application
REM This script sets up and runs the entire project

echo.
echo ======================================
echo  Real Estate Application - Quick Start
echo ======================================
echo.

REM Check if PostgreSQL is running
echo [1/5] Checking PostgreSQL...
psql -U akarsh_user -d real_estate -c "SELECT 1" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL is not running or credentials are wrong!
    echo Please ensure PostgreSQL is running and database "real_estate" exists.
    pause
    exit /b 1
)
echo ✓ PostgreSQL is running

REM Check if Python virtual environment exists
echo.
echo [2/5] Checking Python virtual environment...
if not exist "backend_env" (
    echo Creating virtual environment...
    python -m venv backend_env
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment and install dependencies
echo.
echo [3/5] Installing/updating Python dependencies...
call backend_env\Scripts\Activate.ps1
if %errorlevel% neq 0 (
    REM If PowerShell activation fails, try batch activation
    call backend_env\Scripts\activate.bat
)
pip install -q fastapi uvicorn sqlalchemy psycopg2-binary python-jose cryptography python-multipart passlib pydantic email-validator joblib pandas numpy scikit-learn xgboost lightgbm ollama 2>nul
echo ✓ Python dependencies ready

REM Check if Node modules exist
echo.
echo [4/5] Checking Node.js dependencies...
if not exist "node_modules" (
    echo Installing npm packages...
    npm install --legacy-peer-deps >nul 2>&1
    echo ✓ Node.js dependencies installed
) else (
    echo ✓ Node.js dependencies exist
)

REM Summary
echo.
echo [5/5] Setup complete!
echo.
echo ======================================
echo  Next Steps - Open 3 Terminal Windows
echo ======================================
echo.
echo TERMINAL 1 - Backend (FastAPI):
echo   cd backend
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo TERMINAL 2 - Frontend (React):
echo   npm start
echo.
echo TERMINAL 3 - Chatbot (Optional):
echo   ollama serve
echo.
echo ======================================
echo.
echo After all three are running:
echo   Open browser: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo.
echo ======================================
echo.
pause
