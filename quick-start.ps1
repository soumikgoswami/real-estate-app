# Real Estate Application - PowerShell Quick Start Script
# Run this script to set up and verify all dependencies

Write-Host ""
Write-Host "======================================"
Write-Host "  Real Estate Application Setup"
Write-Host "======================================"
Write-Host ""

# Set Error Action
$ErrorActionPreference = "Continue"

# Step 1: Check PostgreSQL
Write-Host "[1/5] Checking PostgreSQL..." -ForegroundColor Cyan
try {
    $result = psql -U akarsh_user -d real_estate -c "SELECT 1" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
    } else {
        Write-Host "✗ PostgreSQL connection failed" -ForegroundColor Red
        Write-Host "  Please ensure:" -ForegroundColor Yellow
        Write-Host "  1. PostgreSQL service is running"
        Write-Host "  2. Database 'real_estate' exists"
        Write-Host "  3. User 'akarsh_user' exists with password 'repwinfosys_2025'"
        Read-Host "Press Enter to continue anyway..."
    }
} catch {
    Write-Host "✗ PostgreSQL check failed: $_" -ForegroundColor Yellow
}

# Step 2: Create Python Virtual Environment
Write-Host ""
Write-Host "[2/5] Setting up Python virtual environment..." -ForegroundColor Cyan
if (-Not (Test-Path "backend_env")) {
    Write-Host "  Creating new virtual environment..."
    python -m venv backend_env
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Step 3: Activate and install dependencies
Write-Host ""
Write-Host "[3/5] Installing Python dependencies..." -ForegroundColor Cyan
& ".\backend_env\Scripts\Activate.ps1"
$packages = @(
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2-binary",
    "python-jose[cryptography]",
    "python-multipart",
    "passlib[bcrypt]",
    "pydantic",
    "email-validator",
    "joblib",
    "pandas",
    "numpy",
    "scikit-learn",
    "xgboost",
    "lightgbm",
    "ollama"
)

Write-Host "  Installing packages (this may take a moment)..."
pip install --quiet @packages 2>$null
Write-Host "✓ Python packages installed" -ForegroundColor Green

# Step 4: Check Node.js
Write-Host ""
Write-Host "[4/5] Checking Node.js and npm..." -ForegroundColor Cyan
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✓ Node.js $nodeVersion and npm $npmVersion found" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install from https://nodejs.org/" -ForegroundColor Red
}

# Step 5: Install npm packages
Write-Host ""
Write-Host "[5/5] Installing Node.js dependencies..." -ForegroundColor Cyan
if (-Not (Test-Path "node_modules")) {
    Write-Host "  Installing npm packages (this may take a moment)..."
    npm install --legacy-peer-deps | Out-Null
    Write-Host "✓ npm packages installed" -ForegroundColor Green
} else {
    Write-Host "✓ npm packages already installed" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "======================================"
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "======================================"
Write-Host ""
Write-Host "Next Steps - Open 3 Separate PowerShell Windows:" -ForegroundColor Yellow
Write-Host ""
Write-Host "WINDOW 1 - Backend (FastAPI):" -ForegroundColor Cyan
Write-Host "  cd backend"
Write-Host "  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
Write-Host ""
Write-Host "WINDOW 2 - Frontend (React):" -ForegroundColor Cyan
Write-Host "  npm start"
Write-Host ""
Write-Host "WINDOW 3 - Chatbot (Optional):" -ForegroundColor Cyan
Write-Host "  ollama serve"
Write-Host ""
Write-Host "======================================"
Write-Host ""
Write-Host "After all are running:" -ForegroundColor Green
Write-Host "  🌐 Open browser: http://localhost:3000"
Write-Host "  📖 API Docs: http://localhost:8000/docs"
Write-Host ""
Write-Host "======================================"
Write-Host ""
Write-Host "Project Setup Instructions:" -ForegroundColor Cyan
Write-Host "  1. Review PROJECT_SETUP_GUIDE.md for detailed instructions"
Write-Host "  2. Ensure PostgreSQL credentials in backend/app/db.py match your setup"
Write-Host "  3. Place trained model at: backend/models/pipeline_v1.pkl"
Write-Host ""

Read-Host "Press Enter to exit"
