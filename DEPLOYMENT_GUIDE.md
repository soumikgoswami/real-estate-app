# 🚀 DEPLOYMENT GUIDE - Real Estate Platform

Deploy your application to the cloud in **45 minutes** using Vercel (Frontend) + Railway (Backend + Database).

---

## 📋 PREREQUISITES

- ✅ GitHub account (free at https://github.com)
- ✅ Railway account (free at https://railway.app)
- ✅ Vercel account (free at https://vercel.com)
- ✅ Your project code in GitHub

**First time?** Follow these steps in order.

---

## PART 1: Push Code to GitHub (10 minutes)

### Step 1.1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `real-estate-app`
3. Description: "Real Estate Prediction Platform"
4. Public or Private (your choice)
5. Click "Create Repository"
6. Copy the URL (e.g., `https://github.com/your-username/real-estate-app.git`)

### Step 1.2: Push Your Code to GitHub

In PowerShell, navigate to your project and run:

```powershell
cd c:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Real Estate Platform"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/soumikgoswami/real

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify:** Go to your GitHub repo URL and confirm all files are there.

---

## PART 2: Deploy Backend to Railway (15 minutes)

### Step 2.1: Create Railway Project

1. Go to https://railway.app and sign up (free)
2. Click "Create New Project"
3. Select "Deploy from GitHub"
4. Select your `real-estate-app` repository
5. Click "Deploy"

Railway will auto-detect Python and install dependencies.

### Step 2.2: Set Up PostgreSQL on Railway

1. In your Railway project, click "Add Service"
2. Select "PostgreSQL"
3. Railway creates a database automatically

### Step 2.3: Configure Backend Environment Variables

In Railway project dashboard:

1. Go to your Python/FastAPI service
2. Click "Variables" tab
3. Add these environment variables:

```
DB_USER=postgres
DB_PASS=[Railway will show this in PostgreSQL service variables]
DB_HOST=[Railway PostgreSQL host - copy from PostgreSQL service variables]
DB_PORT=5432
DB_NAME=real_estate
SECRET_KEY=7c60338a79efd487573e5af99ecf9266fc6eefee22f15bad7f1fac8ec90b2eed
PIPELINE_PATH=/app/backend/models/pipeline_v1.pkl
```

**How to get PostgreSQL variables from Railway:**
1. Click on PostgreSQL service
2. Go to "Variables" tab
3. Copy `PGHOST`, `PGUSER`, `PGPASSWORD` values

### Step 2.4: Update Backend Start Command

In Railway Python service settings, set the start command:

```
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

(Railway sets $PORT automatically)

### Step 2.5: Get Your Backend URL

1. Go back to FastAPI service
2. Click "Deployments" → latest deployment
3. Copy the domain (e.g., `https://your-app-abc123.railway.app`)

**Test it:** Open `https://your-app-abc123.railway.app/docs` in browser
- You should see the Swagger API docs
- If it loads → ✅ Backend is live!

---

## PART 3: Deploy Frontend to Vercel (10 minutes)

### Step 3.1: Update Frontend API URL

Edit `.env` file in your project root:

```
REACT_APP_API_URL=https://your-app-abc123.railway.app
```

Replace `your-app-abc123.railway.app` with your actual Railway backend URL from Step 2.5.

Push to GitHub:
```powershell
git add .env
git commit -m "Update API URL for production"
git push origin main
```

### Step 3.2: Deploy to Vercel

1. Go to https://vercel.com and sign up (free)
2. Click "Import Project"
3. Select "Import Git Repository"
4. Choose your GitHub repo `real-estate-app`
5. Click "Import"
6. Vercel auto-detects React configuration
7. Click "Deploy"

**Wait for:** Green checkmark and "Deployment Successful"

### Step 3.3: Get Your Frontend URL

After deployment:
- Vercel shows a live URL (e.g., `https://real-estate-app.vercel.app`)
- Click it to open your live app

**Test it:** Open the URL in browser
- Should see your home page
- Try register/login
- If working → ✅ Frontend is live!

---

## PART 4: Verify Everything Works (5 minutes)

### Test Complete Flow

1. **Open frontend:** `https://your-vercel-url.vercel.app`
2. **Register as buyer**
   - Email: `buyer@test.com`
   - Password: `test123`
3. **Register as seller**
   - Email: `seller@test.com`
   - Password: `test123`
4. **Login as seller** → Create property
5. **Login as buyer** → See property, add to favorites
6. **Test API:** `https://your-backend-url.railway.app/docs`

If all steps work → ✅ **You're deployed!**

---

## 🎯 YOUR LIVE APPLICATION

| Service | URL |
|---------|-----|
| **Frontend** | https://your-vercel-url.vercel.app |
| **Backend API** | https://your-backend-url.railway.app |
| **API Docs** | https://your-backend-url.railway.app/docs |
| **Database** | Managed by Railway (PostgreSQL) |

---

## 📊 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────┐
│  User's Browser                 │
│  https://real-estate.vercel.app │
│  (React Frontend - Vercel)      │
└──────────────────┬──────────────┘
                   │ HTTPS
                   ▼
┌──────────────────────────────────┐
│  FastAPI Backend (Railway)       │
│  https://api.railway.app         │
│  - REST API Endpoints            │
│  - Authentication                │
│  - Business Logic                │
└──────────────────┬───────────────┘
                   │ TCP/5432
                   ▼
┌──────────────────────────────────┐
│  PostgreSQL Database (Railway)   │
│  - Users, Properties, Reviews    │
│  - Automated backups             │
└──────────────────────────────────┘
```

---

## 🔒 SECURITY CHECKLIST

- [ ] Don't commit secrets to GitHub (use .env and .gitignore)
- [ ] Update SECRET_KEY in production
- [ ] Enable HTTPS (automatic on Vercel & Railway)
- [ ] Set CORS origins to your frontend domain
- [ ] Use strong database password
- [ ] Monitor logs for errors

---

## 🆘 TROUBLESHOOTING

### Frontend shows blank page
- Check browser console (F12) for errors
- Verify `REACT_APP_API_URL` is correct in `.env`
- Rebuild: go to Vercel → Deployments → Redeploy

### Backend API not responding
- Check Railway logs: Go to service → Logs tab
- Verify all environment variables are set
- Check database connection: Railway → PostgreSQL → variables

### Database connection fails
- Verify `DB_HOST`, `DB_USER`, `DB_PASS` match Railway values
- Check that PostgreSQL service is running (Railway dashboard)
- Restart the service if needed

### CORS errors
- Error: "Access to XMLHttpRequest has been blocked by CORS policy"
- Fix: Update CORS origins in `backend/app/main.py`:

```python
origins = [
    "http://localhost:3000",
    "https://your-vercel-url.vercel.app",  # Add your Vercel URL
]
```

Push this change to GitHub and redeploy on Railway.

---

## 📈 NEXT STEPS

### Monitor Your Application

1. **Railway Dashboard:** Check logs and performance
2. **Vercel Analytics:** Click your project → Analytics tab
3. **Set up email alerts:** Railway sends alerts for errors/downtime

### Scale Your Application

- **Add more resources:** Railway → Service settings → increase resources
- **Enable auto-scaling:** Railway → Variables → set concurrency
- **Database backups:** Railway → PostgreSQL → enable automated backups

### Custom Domain

**Add your own domain** (e.g., `realestate.yourcompany.com`):

**For Frontend (Vercel):**
1. Buy domain from GoDaddy, Namecheap, etc.
2. Vercel project → Settings → Domains
3. Add your domain and follow DNS instructions

**For Backend (Railway):**
1. Add custom domain in Railway → project settings
2. Follow Railway's DNS configuration

---

## 💰 COST BREAKDOWN

| Service | Free Tier | Limits | Cost if exceeding |
|---------|-----------|--------|-------------------|
| **Vercel** | 100GB/month bandwidth | Deployments unlimited | $20/month for Pro |
| **Railway** | $5 free credit/month | Limited resources | $5-50/month |
| **PostgreSQL** | Included in Railway | 1GB storage free | Included in Railway |
| **TOTAL** | FREE | Suitable for 100K+ users | ~$10-15/month |

---

## 🎉 DEPLOYMENT COMPLETE!

Your real estate platform is now live on the internet! 🚀

**Share your app:**
```
Frontend: https://your-vercel-url.vercel.app
API Docs: https://your-backend-url.railway.app/docs
```

---

## 📚 ADDITIONAL RESOURCES

- **Vercel Docs:** https://vercel.com/docs
- **Railway Docs:** https://docs.railway.app
- **FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/
- **React Deployment:** https://create-react-app.dev/deployment/

---

## ⚡ QUICK COMMANDS REFERENCE

```powershell
# Push changes to GitHub
git add .
git commit -m "Your message"
git push origin main

# Vercel will auto-deploy on push
# Railway will auto-deploy on GitHub changes

# Check local backend (before deploying)
cd backend
uvicorn app.main:app --reload

# Check frontend (before deploying)
npm start
```

---

**Questions? Check deployment logs:**
- Railway: Service → Logs tab
- Vercel: Deployments → click deployment → Logs
