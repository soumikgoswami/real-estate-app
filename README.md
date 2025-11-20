# 🏡 Real Estate Prediction Platform

A full-stack web application for real estate property prediction using machine learning, built with React, FastAPI, and PostgreSQL.

## 📸 Features

- **User Authentication**: Separate buyer and seller accounts with JWT-based security
- **Property Listings**: Create, browse, and filter properties
- **Price Prediction**: AI-powered property price prediction using RandomForest + XGBoost ensemble
- **Favorites**: Save and manage favorite properties
- **Reviews**: Anonymous buyer reviews for properties
- **EMI Calculator**: Calculate loan EMI for property purchases
- **Seller Analytics**: Track interested buyers and property performance
- **AI Chatbot**: Real estate Q&A powered by Ollama (TinyLLaMA)
- **Responsive Design**: Mobile-friendly React interface

---

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT + Passlib + bcrypt
- **ML Models**: Scikit-Learn, XGBoost, LightGBM
- **Chatbot**: Ollama (TinyLLaMA)

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Fetch API
- **Styling**: CSS3
- **State Management**: React Hooks

### Infrastructure
- **Database**: PostgreSQL 12+
- **Server**: Uvicorn + FastAPI
- **Dev Tools**: npm, pip, Python venv

---

## ⚡ Quick Start

### Option 1: Automated Setup (Recommended)

**PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\quick-start.ps1
```

**Batch (Command Prompt):**
```cmd
quick-start.bat
```

### Option 2: Manual Setup

#### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

#### 1. Database Setup
```powershell
# Connect to PostgreSQL
psql -U postgres

# Run these commands in psql:
CREATE USER akarsh_user WITH PASSWORD 'repwinfosys_2025';
CREATE DATABASE real_estate OWNER akarsh_user;
GRANT ALL PRIVILEGES ON DATABASE real_estate TO akarsh_user;
\q
```

#### 2. Backend Setup
```powershell
# Create virtual environment
python -m venv backend_env
backend_env\Scripts\Activate.ps1

# Install dependencies
pip install -r backend/requirements.txt

# Start backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```powershell
# In a new terminal
npm install --legacy-peer-deps
npm start
```

#### 4. Chatbot Setup (Optional)
```powershell
# Download Ollama from https://ollama.ai/
ollama pull tinyllama
ollama serve
```

---

## 🎯 Usage

1. **Visit Application**: Open `http://localhost:3000` in your browser
2. **Register**: Create an account as Buyer or Seller
3. **Login**: Use your credentials to access the dashboard

### For Buyers
- 🔍 Browse available properties
- ❤️ Save favorites
- 💰 Calculate EMI for loans
- 📝 Leave reviews on properties
- 💬 Chat with AI assistant

### For Sellers
- ➕ List new properties
- 📊 View analytics (interested buyers, reviews)
- 📈 Track property performance
- 🎯 See which properties are favorited

---

## 📁 Project Structure

```
infosys_internship/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application & routes
│   │   ├── db.py             # Database configuration
│   │   ├── db_init.py        # Database initialization
│   │   ├── models.py         # SQLAlchemy models
│   │   └── featcnt.py        # Feature processing
│   ├── models/               # Trained ML models
│   │   └── pipeline_v1.pkl
│   └── requirements.txt      # Python dependencies
│
├── src/                       # React Frontend
│   ├── components/
│   │   ├── Auth/             # Login & Register
│   │   ├── Buyer/            # Buyer Dashboard
│   │   ├── Seller/           # Seller Dashboard
│   │   └── shared/           # ChatBot, PropertyCard, etc.
│   ├── pages/                # Home, EMI Calculator
│   ├── services/             # API client
│   ├── utils/                # Helper functions
│   ├── App.js                # Main component
│   └── index.js              # Entry point
│
├── public/                    # Static files
├── RE_train.ipynb            # ML model training notebook
├── clean_dataset.py          # Data cleaning script
├── PROJECT_SETUP_GUIDE.md    # Detailed setup guide
└── README.md                 # This file
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Properties
- `GET /api/properties` - List all properties
- `POST /api/properties` - Create property (seller only)
- `POST /api/predict_bulk` - Get price predictions

### Favorites
- `GET /api/favourites` - Get user's favorites
- `POST /api/favourites` - Add to favorites
- `DELETE /api/favourites/{id}` - Remove favorite

### Reviews
- `GET /api/reviews/{property_id}` - Get property reviews
- `POST /api/reviews` - Submit review (buyer only)

### Analytics
- `GET /api/seller/analytics` - Get seller dashboard data

### Chatbot
- `POST /chatbot` - Chat with AI
- `POST /chatbot/stream` - Stream chat response

📖 **Full API Documentation**: `http://localhost:8000/docs`

---

## 🚀 Running the Application

### Start All Services (Recommended: 3 Terminal Windows)

**Terminal 1 - Backend:**
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
npm start
```

**Terminal 3 - Chatbot (Optional):**
```powershell
ollama serve
```

### Access Points
- 🌐 **Frontend**: `http://localhost:3000`
- 🔌 **Backend API**: `http://localhost:8000`
- 📖 **API Documentation**: `http://localhost:8000/docs`
- 🤖 **Chatbot**: Built-in at `http://localhost:3000`

---

## 🔧 Configuration

### Database Connection (backend/app/db.py)
```python
DB_USER = os.getenv("DB_USER", "akarsh_user")
DB_PASS = os.getenv("DB_PASS", "repwinfosys_2025")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "real_estate")
```

### Environment Variables (.env)
Create `.env` file in backend directory:
```env
DB_USER=your_postgres_user
DB_PASS=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=real_estate
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
```

---

## 📊 Machine Learning Model

The application includes a pre-trained ensemble model for price prediction:

**Model Components:**
- Random Forest (150 trees, max_depth=20)
- LightGBM (300 estimators, learning_rate=0.05)
- XGBoost (300 estimators, learning_rate=0.05)
- Ridge Regression (meta-learner)

**Features Used:** 42 engineered features
- Area, BHK, Furnishing status
- Price per BHK, Price per Bath
- Locality & City encoding
- Demand density
- Distance from city center

**Model Performance:**
- MAE: ~132K INR (LightGBM)
- RMSE: ~608K INR
- R² Score: 99.9%

To train a new model, use the notebook `RE_train.ipynb`

---

## 🐛 Troubleshooting

### PostgreSQL Issues
```
Error: could not connect to server
```
**Solution**: Ensure PostgreSQL is running
```powershell
pg_ctl -D "C:\Program Files\PostgreSQL\16\data" restart
```

### Port Already in Use
```
Address already in use: ('0.0.0.0', 8000)
```
**Solution**: Kill the process or use different port
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Dependencies Install Fails
```
pip install -r requirements.txt
```
If fails, try:
```powershell
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### React App Won't Start
```
npm ERR! Could not resolve dependency
```
**Solution**:
```powershell
rm -r node_modules
npm install --legacy-peer-deps
```

---

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/docs/
- **Ollama**: https://ollama.ai/
- **Scikit-Learn**: https://scikit-learn.org/

---

## 📝 Data Processing

### Cleaning Dataset
If you have raw property data:
```powershell
python clean_dataset.py
```
This generates `cleaned_indian_property.csv`

### Training ML Model
1. Open `RE_train.ipynb` in Jupyter Notebook
2. Upload cleaned data or connect to Google Drive
3. Run all cells to train the ensemble model
4. Save the pipeline: `backend/models/pipeline_v1.pkl`

---

## ✅ Deployment Checklist

- [ ] PostgreSQL database created and configured
- [ ] Python dependencies installed
- [ ] Node.js dependencies installed
- [ ] Backend environment variables set
- [ ] Frontend `.env` configured
- [ ] ML model pipeline saved
- [ ] Ollama (optional) installed and running
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Database connection verified
- [ ] All API endpoints accessible
- [ ] User registration and login working
- [ ] Can create/view properties
- [ ] Price prediction working
- [ ] Chatbot responding (if Ollama running)

---

## 📧 Support

For issues or questions:
1. Check `PROJECT_SETUP_GUIDE.md` for detailed instructions
2. Review API documentation at `/docs`
3. Check browser console for frontend errors
4. Check terminal for backend errors
5. Verify all services are running on correct ports

---

## 📄 License

This project is part of the Infosys Internship Program.

---

## 👥 Contributors

- **Backend**: FastAPI, ML Pipeline, Chatbot
- **Frontend**: React Dashboard, Components
- **Database**: PostgreSQL, SQLAlchemy ORM
- **ML**: XGBoost, LightGBM, Scikit-Learn

---

## 🎉 Ready to Go!

Your real estate platform is now ready to use. Start by:
1. Running the quick-start script
2. Registering a test account
3. Exploring the application
4. Testing all features

Happy coding! 🚀
