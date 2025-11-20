# Quick Start Guide - ML Pipeline

## What's New
✅ **ML Pipeline converted from notebook to reusable class-based architecture**
- Modular methods for each pipeline stage
- Easy to retrain or modify individual components
- Production-ready with error handling and logging

## File: `train_model.py`

### Class: `RealEstatePipeline`
A complete ML training pipeline with the following public methods:

```python
# Core pipeline execution
.run_full_pipeline(cleaned_file)  # Run everything at once

# Individual stages (can be chained)
.load_data(cleaned_file)
.validate_data()
.engineer_features()
.prepare_features()
.split_data(test_size=0.2, random_state=42)
.train_baseline_models()
.evaluate_models()
.train_stacking_ensemble()
.print_feature_importance(top_n=15)
.save_model()
```

### Quick Usage

```python
from train_model import RealEstatePipeline

# One-liner training
pipeline = RealEstatePipeline(r"C:\path\to\project").run_full_pipeline(cleaned_file_path)

# Result: Models saved to backend/models/
```

## Running the Pipeline

### Terminal
```bash
cd C:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main
.\backend_env\Scripts\Activate.ps1
python train_model.py
```

### Output Files
- `backend/models/pipeline_v1.pkl` - Trained StackingRegressor (2.96 MB)
- `backend/models/scaler.pkl` - Feature scaler (2.76 KB)
- `backend/models/features.pkl` - Feature names (692 B)

## Model Performance

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| Ridge | 1.47M | 2.49M | 0.983 |
| RandomForest | 46.8K | 233K | 0.9999 |
| LightGBM | 219.8K | 694K | 0.999 |
| XGBoost | 260.6K | 1.13M | 0.997 |
| **Ensemble** | **53K** | **233.6K** | **0.9998** |

## Backend Status

✅ **Server Running** 
- URL: http://0.0.0.0:8000
- Model: StackingRegressor loaded ✓
- Status: Ready for predictions

To restart server:
```bash
cd backend
.\..\..\backend_env\Scripts\Activate.ps1
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Features Used (42 Total)

### Numerical (13)
- area_num, bhk, listing_domain_score, is_furnished, is_rera_registered
- is_apartment, price_per_bhk, area_per_bhk, price_per_bath
- demand_density, price_dev_locality, luxury_index, dist_city_center

### Categorical
- Localities (top 20) - 19 one-hot features
- Cities (top 10) - 7 one-hot features  
- Area categories - 2 one-hot features

## Data Pipeline
```
Makaan_Properties_Buy.csv (320K rows)
            ↓
clean_dataset.py (preprocessing)
            ↓
cleaned_indian_property.csv (231K rows)
            ↓
train_model.py (pipeline)
            ↓
backend/models/pipeline_v1.pkl (trained)
            ↓
backend/app/main.py (serving predictions)
```

## Next Actions

1. **Test Backend** 
   ```bash
   curl http://localhost:8000/docs
   ```

2. **Frontend Setup**
   ```bash
   npm install --legacy-peer-deps
   npm start
   ```

3. **End-to-End Testing**
   - Register as buyer/seller
   - Create property listing
   - Test price prediction
   - Submit reviews

## Key Methods Explained

### `.engineer_features()`
Creates domain-specific features:
- Price ratios (per sqft, per BHK, per bathroom)
- Locality demand density
- Price deviation from locality mean
- Distance from city center (Haversine formula)
- Luxury index (bathrooms, furnishing, domain score)

### `.train_baseline_models()`
Trains 4 base learners:
- Ridge (linear)
- RandomForest (tree ensemble)
- LightGBM (gradient boosting)
- XGBoost (extreme gradient boosting)

### `.train_stacking_ensemble()`
Creates meta-model:
- Base learners: RF, LGB, XGB
- Final estimator: Ridge regression
- Cross-validation: 3-fold
- Ensemble learns how to best combine base predictions

## Troubleshooting

**Error: "Can't get attribute 'DummyPipeline'"**
→ Delete old placeholder model, retrain
```bash
rm backend/models/pipeline_v1.pkl
python train_model.py
```

**Error: Unicode encoding on Windows**
→ Already fixed in train_model.py with:
```python
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

**Slow training?**
→ Reduce model complexity by modifying:
- `n_estimators` (fewer trees)
- `max_depth` (shallower trees)
- `cv` (fewer folds in stacking)

## Architecture Insight
The pipeline is designed as a **decorator pattern** of chained methods:
```python
RealEstatePipeline(root)
    .load_data(file)
    .validate_data()
    .engineer_features()
    ... (each returns self for chaining)
    .run_full_pipeline() (or run sequentially)
```

This allows:
- Modularity: Use individual methods as needed
- Flexibility: Add new stages between existing ones
- Debugging: Inspect data after each stage
- Production: One-line full execution

---
**Status:** ✅ Complete and Production-Ready
**Ensemble R² Score:** 0.9998 (99.98% variance explained)
