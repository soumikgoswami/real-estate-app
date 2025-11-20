# 🎬 Step-by-Step Installation Guide (Video Format)

## Complete Setup Instructions for Real Estate Platform

---

## ⏱️ Total Time: ~30 minutes

### Prerequisites Installation: ~10 min
### Project Setup: ~15 min  
### Testing: ~5 min

---

## 📋 PART 1: Prerequisites Check (5 minutes)

### Step 1.1: Check Python Installation
```powershell
# Open PowerShell and run:
python --version
```
**Expected Output:** `Python 3.8.0` or higher
- If not found: Download from https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation

### Step 1.2: Check Node.js Installation
```powershell
node --version
npm --version
```
**Expected Output:** Node v14+ and npm v6+
- If not found: Download from https://nodejs.org/

### Step 1.3: Check PostgreSQL Installation
```powershell
psql --version
```
**Expected Output:** `psql (PostgreSQL) 12.0` or higher
- If not found: Download from https://www.postgresql.org/download/
- **Important**: Remember your PostgreSQL password

---

## 📋 PART 2: Database Setup (5 minutes)

### Step 2.1: Start PostgreSQL Service
**Windows:**
1. Open Services (Ctrl+R → "services.msc")
2. Find "postgresql-x64-##" service
3. If stopped, right-click → Start

**Or use Command Line:**
```powershell
'C:\Program Files\PostgreSQL\18\bin\pg_ctl.exe' -D "C:\Program Files\PostgreSQL\18\data" start
```

### Step 2.2: Connect to PostgreSQL
```powershell
psql -U postgres
```
**Note:** It will ask for password (set during PostgreSQL installation)

### Step 2.3: Create Database and User
Once connected to psql, run these commands:
```sql
CREATE USER soumik_user WITH PASSWORD 'repwinfosys_2025';
CREATE DATABASE real_estate OWNER soumik_user;
GRANT ALL PRIVILEGES ON DATABASE real_estate TO soumik_user;
\q
```

### Step 2.4: Verify Database Creation
```powershell
psql -U soumik_user -d real_estate -c "SELECT 1"
```
**Expected Output:** Should return `1` (means connection successful)

---

## 📋 PART 3: Backend Setup (10 minutes)

### Step 3.1: Navigate to Project Directory
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
```

### Step 3.2: Create Python Virtual Environment
```powershell
python -m venv backend_env
```
**Wait for:** ~30 seconds to complete

### Step 3.3: Activate Virtual Environment
```powershell
backend_env\Scripts\Activate.ps1
```
**Expected:** Command prompt changes to show `(backend_env)`

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
backend_env\Scripts\Activate.ps1
```

### Step 3.4: Install Python Dependencies
```powershell
pip install -r backend/requirements.txt
```
**Wait for:** ~3-5 minutes (downloading packages)

### Step 3.5: Verify Installation
```powershell
python -c "import fastapi; print('FastAPI OK')"
python -c "import sqlalchemy; print('SQLAlchemy OK')"
python -c "import pandas; print('Pandas OK')"
```
**Expected Output:** All three print "OK"

### Step 3.6: Test Backend Server
```powershell
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Wait for output like:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Test in browser:**
- Open: `http://localhost:8000`
- Expected: `{"message": "🏡 Real Estate Prediction API is running successfully!"}`
- API Docs: `http://localhost:8000/docs`

**Stop Backend:** Press `Ctrl+C`

---

## 📋 PART 4: Frontend Setup (8 minutes)

### Step 4.1: Open New PowerShell Window
**Important:** Keep backend running, open new terminal

### Step 4.2: Navigate to Project
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
```

### Step 4.3: Install npm Dependencies
```powershell
npm install --legacy-peer-deps
```
**Wait for:** ~2-3 minutes

**If you get errors:**
```powershell
npm cache clean --force
npm install --legacy-peer-deps
```

### Step 4.4: Create React Environment File
Create file `.env` in project root:
```
REACT_APP_API_URL=http://localhost:8000
```

### Step 4.5: Start React Development Server
```powershell
npm start
```

**Wait for:**
```
webpack compiled...
Compiled successfully!
```

**Browser should auto-open to:** `http://localhost:3000`

---

## 📋 PART 5: Optional - Chatbot Setup (5 minutes)

### Step 5.1: Download Ollama
- Visit: https://ollama.ai/
- Download and install for Windows

### Step 5.2: Open New PowerShell Window

### Step 5.3: Pull TinyLLaMA Model
```powershell
ollama pull tinyllama
```
**Wait for:** ~2-3 minutes (downloading model)

### Step 5.4: Start Ollama Service
```powershell
ollama serve
```

**Expected:**
```
time=2024-01-01T00:00:00.000Z level=INFO msg="Ollama is running"
```

---

## ✅ PART 6: Testing Everything (5 minutes)

### Step 6.1: Check All Services Running

**Service Checklist:**
- [ ] PostgreSQL running (Services → postgresql)
- [ ] Backend running (Terminal 1: localhost:8000)
- [ ] Frontend running (Terminal 2: localhost:3000)
- [ ] Ollama running (Terminal 3: localhost:11434) - Optional

### Step 6.2: Test Frontend
1. Open `http://localhost:3000`
2. You should see the home page
3. Try the "Register" button

### Step 6.3: Test API
```powershell
# In new PowerShell window:
$response = Invoke-WebRequest -Uri "http://localhost:8000" -Method Get
$response.Content | ConvertFrom-Json | Format-List
```

### Step 6.4: Test Database
```powershell
psql -U soumik_user -d real_estate -c "\dt"
```
**Should show empty tables** (will be created when you first interact with app)

### Step 6.5: Test Complete Flow
1. Register → Create account as Buyer
2. Login → See dashboard
3. Register another → Create account as Seller
4. Login as Seller → List a property
5. Login as Buyer → See property, add to favorites
6. Try EMI Calculator
7. Try Chatbot (if Ollama running)

---

## 🚀 RUNNING DAILY (After Setup)

Once everything is set up, to run the project daily:

### Daily Start (3 PowerShell Windows)

**Window 1 - Backend:**
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
backend_env\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Window 2 - Frontend:**
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
npm start
```

**Window 3 - Chatbot (Optional):**
```powershell
ollama serve
```

**Then:** Open `http://localhost:3000` in browser

---

## 🔧 Troubleshooting Quick Fixes

### Issue: "PostgreSQL connection refused"
```
Solution:
1. Open Services
2. Find "postgresql-x64-##"
3. Right-click → Properties
4. Change "Startup type" to "Automatic"
5. Click Start
```

### Issue: "port 8000 already in use"
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID_number> /F
```

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
```powershell
backend_env\Scripts\Activate.ps1  # Make sure venv is activated
pip install fastapi uvicorn
```

### Issue: "npm ERR! Could not resolve dependency"
```powershell
npm cache clean --force
npm install --legacy-peer-deps
```

### Issue: "Cannot find module 'react-router-dom'"
```powershell
npm install react-router-dom
```

### Issue: "Chatbot not responding"
```
1. Make sure Ollama is running in Window 3
2. Check: http://localhost:11434/api/tags
3. If error, reinstall: ollama pull tinyllama
```

---

## 📱 Features to Test

Once everything is running:

### ✅ Buyer Features
- [ ] Register as buyer
- [ ] Login
- [ ] Browse properties (initially empty)
- [ ] Add property to favorites
- [ ] Use EMI Calculator (calculate loan payment)
- [ ] Leave review on property (anonymous)
- [ ] Use chatbot for real estate questions

### ✅ Seller Features
- [ ] Register as seller
- [ ] Login
- [ ] Create new property listing
- [ ] Upload property images
- [ ] View seller analytics (interested buyers)
- [ ] See reviews from buyers

### ✅ ML Features
- [ ] Price prediction for property
- [ ] Works with uploaded CSV data

### ✅ Chatbot Features
- [ ] Ask about RERA registration
- [ ] Ask about home loans
- [ ] Ask about property documents
- [ ] Ask about investment tips

---

## 📊 Project Structure Check

After setup, your folder should look like:

```
infosys_internship-main/
├── backend/
│   ├── app/
│   │   ├── main.py ✓
│   │   ├── db.py ✓
│   │   └── models.py ✓
│   ├── requirements.txt ✓
│   └── .env (optional)
├── src/ ✓
│   ├── App.js ✓
│   └── index.js ✓
├── node_modules/ ✓ (created by npm install)
├── backend_env/ ✓ (created by python -m venv)
├── README.md ✓
├── PROJECT_SETUP_GUIDE.md ✓
└── quick-start.ps1 ✓
```

---

## 🎯 Next Steps After Setup

1. **Explore Code:**
   - Review `backend/app/main.py` (API endpoints)
   - Review `src/App.js` (Frontend routes)
   - Review `src/components/` (UI components)

2. **Training ML Model:**
   - Open `RE_train.ipynb` in Jupyter
   - Follow cells to train on property data
   - Save model to `backend/models/pipeline_v1.pkl`

3. **Deploy to Production:**
   - Consider Docker for containerization
   - Use gunicorn instead of uvicorn for production
   - Deploy frontend to Vercel/Netlify
   - Deploy backend to Render/Railway/AWS

4. **Customize:**
   - Update colors in `src/App.css`
   - Add more cities to property listing
   - Extend chatbot FAQ responses
   - Add more ML features

---

## 📞 Getting Help

1. **Check Logs:**
   - Backend: Look at terminal output
   - Frontend: Check browser console (F12)
   - Database: Check PostgreSQL logs

2. **Common Errors:**
   - See "Troubleshooting" section above
   - Check all 3 services are running
   - Verify ports are correct (8000, 3000, 11434)

3. **API Documentation:**
   - Go to `http://localhost:8000/docs`
   - Try endpoints directly from browser

---

## ✨ Congratulations!

You now have a fully functional real estate platform running locally! 🎉

**Next Steps:**
1. Create test accounts (buyer + seller)
2. Test all features
3. Review the code
4. Consider customizations
5. Plan for deployment

---

## 📚 Additional Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React Hooks**: https://react.dev/reference/react/hooks
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Machine Learning**: https://scikit-learn.org/

**Happy coding! 🚀**
