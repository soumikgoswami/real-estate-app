# Run Commands (Windows PowerShell)

This file contains copy-paste PowerShell commands to run the backend and frontend in this project on Windows. Use the commands from the project root:

`C:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main`

---

## Backend (FastAPI)

### Activate the backend virtualenv
```powershell
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
. '.\backend_env\Scripts\Activate.ps1'
```

### Install Python requirements (if needed)
```powershell
. '.\backend_env\Scripts\Activate.ps1'
pip install -r backend/requirements.txt
```

### Create DB tables (one-time)
```powershell
. '.\backend_env\Scripts\Activate.ps1'
python -c "from backend.app import db, models; models.Base.metadata.create_all(bind=db.engine); print('Tables created')"
```

### Start backend (foreground)
```powershell
# Runs uvicorn in the current terminal (blocks)
. '.\backend_env\Scripts\Activate.ps1'
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

### Start backend as a detached background process (non-blocking)
```powershell
# Uses venv python to start uvicorn in a new hidden window
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
Start-Process -FilePath '.\backend_env\Scripts\python.exe' -ArgumentList '-m','uvicorn','backend.app.main:app','--host','0.0.0.0','--port','8000' -WorkingDirectory 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System' -WindowStyle Hidden
```

### Stop backend (stop process listening on port 8000)
```powershell
$line = netstat -ano | Select-String ':8000' | Select-Object -First 1
if ($line) {
  $parts = ($line -split '\s+')
  $pid = $parts[-1]
  if ($pid -and $pid -ne '0') { Stop-Process -Id $pid -Force }
}
```

### Health check
```powershell
Invoke-WebRequest -Uri 'http://localhost:8000/' -UseBasicParsing | Select-Object StatusCode, Content
```

---

## Frontend (React)

### Install dependencies (one-time or when package.json changes)
```powershell
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
npm install
```

### Start frontend (foreground)
```powershell
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
npm start
# This will block the terminal and stream the dev server logs
```

### Start frontend in a new visible cmd window (non-blocking, see logs there)
```powershell
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
Start-Process -FilePath 'cmd.exe' -ArgumentList '/c','start','cmd.exe','/k','npm','start' -WorkingDirectory 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
```

### Start frontend detached (background) via Start-Process (no visible logs)
```powershell
cd 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System'
Start-Process -FilePath 'npm' -ArgumentList 'start' -WorkingDirectory 'C:\Users\SOUMIK\Desktop\AI-based_Real_Estate_Management_System' -WindowStyle Hidden
```

### Stop frontend (stop node process on port 3000)
```powershell
$line = netstat -ano | Select-String ':3000' | Select-Object -First 1
if ($line) {
  $parts = ($line -split '\s+')
  $pid = $parts[-1]
  if ($pid -and $pid -ne '0') { Stop-Process -Id $pid -Force }
}
```

### Health check
```powershell
Invoke-WebRequest -Uri 'http://localhost:3000/' -UseBasicParsing -ErrorAction SilentlyContinue | Select-Object StatusCode, Content
```

---

## Other useful commands

### Load ML pipeline quick test
```powershell
. '.\backend_env\Scripts\Activate.ps1'
python -c "import joblib; model = joblib.load('backend/models/pipeline_v1.pkl'); print('Model loaded:', type(model).__name__)"
```

### Insert provided sample data scripts
```powershell
. '.\backend_env\Scripts\Activate.ps1'
python .\scripts\insert_sample_properties.py
python .\scripts\insert_batch_data.py  # bulk insert script (20 sellers x 5 props, 200 buyers by default)
```

### Run quick predict_bulk locally (example)
```powershell
# Fetch properties and predict for first 20
$props = Invoke-RestMethod -Uri 'http://localhost:8000/api/properties' -Method GET
$sample = $props | Select-Object -First 20
$payload = $sample | ForEach-Object { @{ id = $_.id; area_sqft = $_.area_sqft; bhk = $_.bhk; listing_score = $_.listing_score; is_furnished = $_.is_furnished; city_id = $_.city_id } } | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri 'http://localhost:8000/api/predict_bulk' -Method POST -Body $payload -ContentType 'application/json'
```

---

## Notes & Tips
- These commands assume Windows PowerShell (v5.1). Adjust for other shells.
- Use the `Start-Process` approach when you need the current terminal free; open a visible cmd window if you want to watch frontend logs.
- For production-like deployments, consider using a process manager (e.g., `pm2` for Node, `gunicorn`/`uvicorn --workers` behind a reverse proxy) and proper database credentials.
- If `pwd_context.hash()` fails, ensure `bcrypt` and `passlib` versions are compatible (in our dev env we pinned `bcrypt==4.0.1`).

If you want, I can also add a small `run-local.ps1` script that runs both servers and opens the browser automatically.