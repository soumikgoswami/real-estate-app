# AI Coding Agent Instructions - Real Estate Platform

## Architecture Overview

This is a **full-stack real estate prediction platform** with three core layers:

- **Frontend** (React 18): Single Page App with role-based routing (buyer/seller dashboards)
- **Backend** (FastAPI): RESTful API with JWT authentication, database ORM via SQLAlchemy
- **ML Pipeline**: Ensemble model (RandomForest + XGBoost + LightGBM + Ridge) for price prediction
- **Database** (PostgreSQL): User authentication, properties, favorites, reviews
- **Optional**: Ollama TinyLLaMA chatbot for real estate Q&A

## Database & Models

**Key tables** (`backend/app/models.py`):
- `users` (buyer/seller auth, JWT-based)
- `properties` (listings with seller_id foreign key)
- `favourites` (buyer bookmarks)
- `reviews` (anonymous buyer feedback, 1-5 rating)

**Critical patterns:**
- Sellers can only create properties (role check in `/api/properties` POST)
- Buyers can only review properties (role check in `/api/reviews` POST)
- Reviews anonymized to sellers as "Buyer 1", "Buyer 2", etc.
- All endpoints require Bearer token validation via `get_current_user_from_token()`

## Authentication & Security

- JWT tokens with 24-hour expiry (default in `ACCESS_TOKEN_EXPIRE_HOURS`)
- Passwords hashed via bcrypt (`pwd_context.hash()`)
- Token embedded as `{"id", "email", "user_type", "exp"}`
- CORS configured for localhost:3000/3001/5173 for dev (frontend ports)

## API Patterns

All protected endpoints follow this structure:
```python
@app.post("/api/endpoint")
def endpoint(payload, user: dict = Depends(get_current_user_from_token), session: Session = Depends(get_db)):
    if user["user_type"] != "expected_type":
        raise HTTPException(status_code=403, detail="Forbidden")
```

**Common endpoints:**
- Auth: `/api/register`, `/api/login` (returns token + user object)
- Properties: `/api/properties` (GET all with filters; POST for sellers only)
- Favorites: `/api/favourites` (GET, POST add, DELETE)
- Reviews: `/api/reviews/{property_id}` (GET public; POST for buyers only)
- Analytics: `/api/seller/analytics` (GET for sellers - shows interested buyers, review counts per property)

## ML Model Pipeline

**Location**: `backend/models/pipeline_v1.pkl` (pre-trained)

**Flow in `/api/predict_bulk`:**
1. Accept list of `PredictShort` objects (area_sqft, bhk, city_id, etc.)
2. Feature engineering: Creates 42-feature DataFrame with city/area encoding
3. Model predicts prices; multiply by 5 for final price estimate
4. Return predictions as `{"id", "prediction"}` pairs

**Feature set** (`FEATURES_42`): area_num, bhk, furnished status, city encoding (7 cities), area categories, price ratios.

## Frontend Routes & Components

**App-level routing** (`src/App.js`):
- Public: `/`, `/login`, `/register`
- Protected (buyer): `/buyer-dashboard`, `/favourites`, `/emi-calculator`
- Protected (seller): `/seller-dashboard`, `/seller-visited`
- Role redirect: Authenticated users auto-redirected to their dashboard type

**Key components** (`src/components/`):
- `Auth/Login.jsx`, `Auth/Register.jsx` - Form submission to `/api/login` and `/api/register`
- `Buyer/BuyerDashboard.jsx` - Property list from `/api/properties`, add to favorites
- `Seller/SellerDashboard.jsx` - Create property form (POST `/api/properties`), upload images to `/api/upload-image`
- `shared/ChatBot.js` - POST to `/chatbot` (streaming fallback to FAQ if Ollama down)

**State management**: React Hooks (localStorage for token, useState for UI state)

**API client** (`src/services/api.js`): Fetch wrapper with Bearer token in header

## Critical Development Workflows

### Local Development
```powershell
# Terminal 1: Backend
cd backend; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (separate PowerShell window)
npm start

# Terminal 3 (optional): Chatbot
ollama serve
```

**API docs**: `http://localhost:8000/docs` (auto-generated Swagger UI)

### Database Connection
- Uses `backend/app/db.py` config: `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, `DB_NAME` (from env or defaults)
- Connection string: `postgresql://user:pass@localhost:5432/real_estate`
- SQLAlchemy ORM handles table creation on app startup via `Base.metadata.create_all()`

### Testing Workflow
1. Register buyer + seller accounts (different emails)
2. Seller: Create property, upload images
3. Buyer: List properties, add to favorites, submit review
4. Seller: Check analytics dashboard (shows favorite counts, buyer names, reviews)
5. EMI Calculator: Test with various loan amounts
6. Chatbot: Ask about RERA, loans, documents (fallback FAQ if Ollama unavailable)

## Project-Specific Conventions

- **Role-based access**: Always check `user["user_type"]` in seller/buyer-only endpoints
- **Anonymous reviews**: Map reviewer user_id to "Buyer N" for sellers, never expose buyer emails in review responses
- **Soft deletes**: Property status field defaults to 'active' (future for deleted flag)
- **Image uploads**: Stored in `uploads/properties/` with UUID filename, served via `/uploads/properties/{filename}`
- **Fallback chatbot**: `/chatbot` endpoint has FAQ mode when Ollama unreachable (keyword matching on lowercase message)
- **Pipeline assumption**: Code assumes `pipeline_v1.pkl` exists; if missing, prediction endpoint fails with 500

## Common Integration Points

**New endpoints usually need:**
1. Pydantic model for request validation (in `main.py` or separate `schemas.py`)
2. JWT dependency for auth
3. Database session dependency
4. Correct HTTP method + path
5. Role check if buyer/seller only

**Frontend integration:**
1. Add route in `src/App.js` (if new page)
2. Fetch call in `src/services/api.js` or component
3. Token attached via `Authorization: Bearer <token>` header
4. Error handling for 401 (redirect to login) and 403 (permission denied)

## Files to Review First

- `backend/app/main.py` (150+ lines, all endpoints + auth logic)
- `backend/app/models.py` (database schema)
- `src/App.js` (routing structure)
- `src/components/Auth/Login.jsx` (auth flow example)
- `backend/requirements.txt` (dependencies)

## Known Limitations & Quirks

- ML model path is hardcoded (update `PIPELINE_PATH` variable if relocating model)
- Chatbot model name hardcoded to "tinyllama" (change in `ollama.chat()` call if using different model)
- 42 features hardcoded in `FEATURES_42` list; adding features requires retraining model
- No email verification for registration
- No password reset flow
- Reviews and favorites not soft-deleted (permanent upon deletion)
