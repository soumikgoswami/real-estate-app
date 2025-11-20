# 🏡 Real Estate Application - Project Setup & Run Guide

This is a full-stack real estate prediction application with React frontend, FastAPI backend, and PostgreSQL database.

---

## 📋 Project Structure

```
infosys_internship/
├── backend/
│   └── app/
│       ├── __init__.py
│       ├── main.py           # FastAPI application
│       ├── db.py             # Database configuration
│       ├── db_init.py        # Database initialization
│       ├── models.py         # SQLAlchemy models
│       └── featcnt.py        # Feature processing
├── src/                       # React frontend
│   ├── App.js
│   ├── index.js
│   ├── pages/
│   ├── components/
│   ├── services/
│   └── utils/
├── public/
├── RE_train.ipynb            # ML model training notebook
├── clean_dataset.py          # Data cleaning script
└── PROJECT_SETUP_GUIDE.md    # This file
```

---

## 🛠️ Prerequisites

Make sure you have installed:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 14+** ([Download](https://nodejs.org/))
- **PostgreSQL 12+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/))

### Optional but Recommended:
- **Ollama** (for chatbot feature) - [Download](https://ollama.ai/)
- **VS Code** - [Download](https://code.visualstudio.com/)

---

## 📦 Installation Steps

### Step 1: Set Up PostgreSQL Database

1. **Start PostgreSQL** (if not already running)
   - Windows: Open Services → Search for "PostgreSQL" → Start it
   - Or use: `pg_ctl -D "C:\Program Files\PostgreSQL\data" start`

2. **Create Database & User**
   ```powershell
   # Open PowerShell as Administrator
   psql -U postgres
   ```
   
   Then run these SQL commands:
   ```sql
   CREATE USER akarsh_user WITH PASSWORD 'repwinfosys_2025';
   CREATE DATABASE real_estate OWNER akarsh_user;
   GRANT ALL PRIVILEGES ON DATABASE real_estate TO akarsh_user;
   ```
   
   Type `\q` to exit psql.

3. **Initialize Database Tables**
   - The database tables will be auto-created on first backend startup

---

### Step 2: Set Up Backend (FastAPI)

1. **Open PowerShell and navigate to the project:**
   ```powershell
   cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv backend_env
   backend_env\Scripts\Activate.ps1
   ```

3. **Install Python dependencies:**
   ```powershell
   pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] python-multipart passlib[bcrypt] pydantic email-validator joblib pandas numpy scikit-learn xgboost lightgbm ollama
   ```

4. **Configure Backend Settings**
   
   The backend expects PostgreSQL credentials. You can set them as environment variables or they default to:
   - User: `akarsh_user`
   - Password: `repwinfosys_2025`
   - Host: `localhost`
   - Port: `5432`
   - Database: `real_estate`
   
   If your credentials differ, create a `.env` file in the `backend/` folder:
   ```
   DB_USER=your_postgres_user
   DB_PASS=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=real_estate
   ```

5. **Create ML Pipeline Model** (if not already present)
   
   The backend expects a trained model at: `backend/models/pipeline_v1.pkl`
   
   To train the model:
   - Open `RE_train.ipynb` in Jupyter
   - Run all cells (requires `cleaned_indian_property.csv`)
   - The trained pipeline will be saved
   
   Or update the path in `backend/app/main.py` line ~54:
   ```python
   PIPELINE_PATH = "backend/models/pipeline_v1.pkl"  # Update this path
   ```

6. **Start Backend Server**
   ```powershell
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   ✅ Backend should be running at: `http://localhost:8000`
   📖 API Docs available at: `http://localhost:8000/docs`

---

### Step 3: Set Up Frontend (React)

1. **Open a new PowerShell window** and navigate to project:
   ```powershell
   cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
   ```

2. **Install frontend dependencies:**
   ```powershell
   npm install
   ```
   
   If `npm install` fails, try:
   ```powershell
   npm install --legacy-peer-deps
   ```

3. **Create `.env` file in project root:**
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Start React Development Server:**
   ```powershell
   npm start
   ```
   
   ✅ Frontend should open automatically at: `http://localhost:3000`

---

### Step 4: Optional - Set Up Chatbot (Ollama)

The chatbot uses Ollama with TinyLLaMA model.

1. **Download & Install Ollama:**
   - Download from: https://ollama.ai/
   - Install and run it

2. **Pull TinyLLaMA Model:**
   ```powershell
   ollama pull tinyllama
   ```

3. **Start Ollama Service:**
   ```powershell
   ollama serve
   ```
   
   ✅ Ollama will run at `http://localhost:11434`
   
   The backend will automatically connect to it.

---

## 🚀 Running the Complete Application

Once everything is installed, follow these steps in order:

### Terminal 1 - Database
```powershell
# Ensure PostgreSQL is running (it usually auto-starts)
# Check with:
psql -U akarsh_user -d real_estate -c "SELECT 1"
```

### Terminal 2 - Backend (FastAPI)
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
backend_env\Scripts\Activate.ps1
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 3 - Frontend (React)
```powershell
cd c:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
npm start
```

### Terminal 4 - Chatbot (Optional, Ollama)
```powershell
ollama serve
```

---

## 🎯 Testing the Application

### 1. **Register a New User**
   - Go to `http://localhost:3000`
   - Click "Register"
   - Choose "Buyer" or "Seller"
   - Fill in details and register

### 2. **Login**
   - Go to `http://localhost:3000/login`
   - Enter credentials

### 3. **Buyer Features**
   - 🏠 Browse properties
   - ❤️ Save to favorites
   - 💬 Leave reviews
   - 📊 Calculate EMI

### 4. **Seller Features**
   - ➕ List new property
   - 📈 View analytics (interested buyers, favorites)
   - 📊 See reviews

### 5. **AI Chatbot**
   - Click the chatbot icon
   - Ask questions about real estate, RERA, loans, etc.

---

## 📊 Data Processing

### Clean Dataset
If you have a raw CSV file (`Makaan_Properties_Buy.csv`):

```powershell
python clean_dataset.py
```

This generates `cleaned_indian_property.csv`

### Train ML Model
1. Upload cleaned data to Google Drive (if using Colab)
2. Open `RE_train.ipynb` in Jupyter
3. Run all cells
4. Save the trained pipeline model

---

## 🔑 Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/register` | Register new user |
| POST | `/api/login` | Login user |
| POST | `/api/properties` | Create property (seller) |
| GET | `/api/properties` | List properties |
| POST | `/api/favourites` | Add to favorites |
| GET | `/api/favourites` | Get user favorites |
| DELETE | `/api/favourites/{id}` | Remove favorite |
| POST | `/api/reviews` | Add review |
| GET | `/api/reviews/{property_id}` | Get property reviews |
| GET | `/api/seller/analytics` | Seller analytics |
| POST | `/api/predict_bulk` | Predict property prices |
| POST | `/chatbot` | Chat with AI |

📖 **Full API documentation:** `http://localhost:8000/docs`

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error
```
Error: could not connect to server: Connection refused
```
**Solution:** Ensure PostgreSQL is running
```powershell
# Restart PostgreSQL
pg_ctl -D "C:\Program Files\PostgreSQL\16\data" restart
```

### Python Dependency Error
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Ensure virtual environment is activated
```powershell
backend_env\Scripts\Activate.ps1
pip install -r requirements.txt  # if requirements.txt exists
```

### Port Already in Use
```
Address already in use: ('0.0.0.0', 8000)
```
**Solution:** Change port or kill process
```powershell
# Use different port
uvicorn app.main:app --port 8001

# Or kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### React Build Error
```
npm ERR! Could not resolve dependency
```
**Solution:**
```powershell
npm install --legacy-peer-deps
```

### Ollama Not Connecting
If chatbot doesn't work, the app has a fallback to FAQ responses. Ensure Ollama is running on `localhost:11434`.

---

## 📝 Environment Variables

Create a `.env` file in the backend folder:

```env
# Database
DB_USER=akarsh_user
DB_PASS=repwinfosys_2025
DB_HOST=localhost
DB_PORT=5432
DB_NAME=real_estate

# JWT
SECRET_KEY=7c60338a79efd487573e5af99ecf9266fc6eefee22f15bad7f1fac8ec90b2eed
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# ML Model
PIPELINE_PATH=backend/models/pipeline_v1.pkl

# Ollama
OLLAMA_HOST=localhost:11434
```

---

## 📚 Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/docs/

---

## 💡 Quick Commands Reference

| Task | Command |
|------|---------|
| Activate backend env | `backend_env\Scripts\Activate.ps1` |
| Deactivate env | `deactivate` |
| Start backend | `uvicorn app.main:app --reload` |
| Start frontend | `npm start` |
| Install dependencies | `npm install` |
| Run tests | `npm test` |
| Build for production | `npm run build` |
| Access API docs | `http://localhost:8000/docs` |
| Access Swagger UI | `http://localhost:8000/redoc` |

---

## ✅ Final Checklist

- [ ] PostgreSQL installed and running
- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Database `real_estate` created
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] `.env` files configured (if needed)
- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Can access `http://localhost:3000`
- [ ] Can register and login
- [ ] API docs available at `http://localhost:8000/docs`

---

## 🎉 Success!

Your application is now running! Start with:
1. **Register a buyer or seller account**
2. **Explore the dashboard**
3. **Test all features**
4. **Check the chatbot**

---

**Questions?** Check the API documentation at `/docs` or review the code in `backend/app/main.py` and `src/App.js`.
