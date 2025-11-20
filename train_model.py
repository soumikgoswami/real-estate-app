"""
ML Pipeline for Real Estate Price Prediction
Trains ensemble model and saves to backend/models/pipeline_v1.pkl
"""
import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings("ignore")

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class RealEstatePipeline:
    """ML Pipeline for real estate price prediction using stacking ensemble"""
    
    def __init__(self, project_root):
        self.project_root = project_root
        os.chdir(project_root)
        sys.path.insert(0, project_root)
        
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = None
        self.features = None
        self.stacking_regressor = None
        
        print(f"✓ Pipeline initialized at: {os.getcwd()}\n")
    
    def load_data(self, cleaned_file):
        """Load and preprocess the dataset"""
        print("📥 Loading data...")
        if not os.path.exists(cleaned_file):
            print(f"❌ Error: {cleaned_file} not found")
            sys.exit(1)
        
        self.df = pd.read_csv(cleaned_file, encoding="latin1")
        print(f"✓ Loaded dataset: {self.df.shape}")
        
        # Normalize column names
        self.df.columns = self.df.columns.str.strip().str.lower()
        return self
    
    def validate_data(self):
        """Validate core columns and prepare data"""
        print("✓ Validating data...")
        
        # Check required columns
        for col in ["price_num", "area_num", "price_per_sqft"]:
            if col not in self.df.columns:
                print(f"❌ Error: {col} not found in dataset")
                sys.exit(1)
        
        # Create/clean BHK column
        if "bhk" not in self.df.columns:
            if "no_of_bhk" in self.df.columns:
                self.df["bhk"] = self.df["no_of_bhk"].astype(str).str.extract(r'(\d+)')[0].astype(float)
            else:
                self.df["bhk"] = 2.0
        
        self.df = self.df[self.df["bhk"].notna() & (self.df["bhk"] > 0)]
        
        # Coerce numerics
        self.df["area_num"] = pd.to_numeric(self.df["area_num"], errors="coerce")
        self.df["price_num"] = pd.to_numeric(self.df["price_num"], errors="coerce")
        self.df = self.df.dropna(subset=["area_num", "price_num"])
        
        print(f"✓ Data validated: {self.df.shape[0]} rows")
        return self
    
    def engineer_features(self):
        """Engineer all features"""
        print("⚙️  Engineering features...")
        
        # Price per sqft
        if "price_per_sqft" not in self.df.columns:
            self.df["price_per_sqft"] = self.df["price_num"] / self.df["area_num"]
        
        # Basic derived features
        self.df["price_per_bhk"] = self.df["price_num"] / self.df["bhk"]
        self.df["area_per_bhk"] = self.df["area_num"] / self.df["bhk"]
        
        # Bath column
        if "bath" in self.df.columns:
            self.df["bath"] = pd.to_numeric(self.df["bath"], errors="coerce").fillna(self.df["bhk"])
        else:
            self.df["bath"] = self.df["bhk"]
        
        self.df["price_per_bath"] = self.df["price_num"] / (self.df["bath"] + 1)
        
        # Demand density
        if "locality_name" in self.df.columns:
            locality_counts = self.df["locality_name"].value_counts().to_dict()
            self.df["demand_density"] = self.df["locality_name"].map(locality_counts).fillna(0).astype(int)
        else:
            self.df["demand_density"] = 0
        
        # Price deviation by locality
        if "locality_name" in self.df.columns:
            local_mean = self.df.groupby("locality_name")["price_per_sqft"].transform("mean")
            self.df["price_dev_locality"] = self.df["price_per_sqft"] - local_mean
        else:
            self.df["price_dev_locality"] = 0
        
        # Luxury index
        self.df["is_furnished"] = self.df.get("is_furnished", 0).astype(str).str.lower().map(
            {"furnished": 1, "unfurnished": 0, "semi-furnished": 0}
        ).fillna(0).astype(int)
        self.df["is_rera_registered"] = self.df.get("is_rera_registered", 0).fillna(0).astype(int)
        self.df["is_apartment"] = self.df.get("is_apartment", 0).fillna(0).astype(int)
        self.df["listing_domain_score"] = self.df.get("listing_domain_score", 0).fillna(0)
        
        self.df["luxury_index"] = (self.df["bath"] / self.df["bhk"]).fillna(0) + self.df["is_furnished"] + self.df["listing_domain_score"]
        
        # Area category
        self.df["area_cat"] = pd.cut(self.df["area_num"], bins=[0, 1000, 2000, 1e9], labels=["small", "medium", "large"])
        
        # Distance from city center
        self.df["dist_city_center"] = self._compute_distances()
        
        print("✓ Features engineered")
        return self
    
    def _compute_distances(self):
        """Compute distance from city centers using haversine formula"""
        def haversine_km(lat1, lon1, lat2, lon2):
            R = 6371.0
            phi1, phi2 = np.radians(lat1), np.radians(lat2)
            dphi = np.radians(lat2 - lat1)
            dlambda = np.radians(lon2 - lon1)
            a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
            return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        
        city_centers = {
            "bangalore": (12.9716, 77.5946),
            "mumbai": (19.0760, 72.8777),
            "delhi": (28.6139, 77.2090),
            "chennai": (13.0827, 80.2707),
            "hyderabad": (17.3850, 78.4867),
            "kolkata": (22.5726, 88.3639),
            "lucknow": (26.8467, 80.9462)
        }
        
        if "latitude" in self.df.columns and "longitude" in self.df.columns:
            self.df["latitude"] = pd.to_numeric(self.df["latitude"], errors="coerce")
            self.df["longitude"] = pd.to_numeric(self.df["longitude"], errors="coerce")
            
            def compute_dist(row):
                city = str(row.get("city_name", "")).lower()
                lat = row["latitude"]
                lon = row["longitude"]
                for k, (clat, clon) in city_centers.items():
                    if k in city:
                        return haversine_km(lat, lon, clat, clon)
                return np.nan
            
            distances = self.df.apply(
                lambda r: compute_dist(r) if pd.notna(r.get("latitude")) and pd.notna(r.get("longitude")) else np.nan,
                axis=1
            )
        else:
            distances = np.nan
        
        return distances.fillna(distances.median() if not pd.Series(distances).isna().all() else 0)
    
    def prepare_features(self):
        """Prepare feature matrix and encode categorical variables"""
        print("🔧 Preparing features...")
        
        base_feats = [
            "area_num", "bhk", "listing_domain_score", "is_furnished", "is_rera_registered", "is_apartment",
            "price_per_bhk", "area_per_bhk", "price_per_bath", "demand_density", "price_dev_locality",
            "luxury_index", "dist_city_center"
        ]
        base_feats = [c for c in base_feats if c in self.df.columns]
        
        # Locality encoding
        loc_cols = []
        if "locality_name" in self.df.columns:
            top_localities = self.df["locality_name"].value_counts().nlargest(20).index
            self.df["locality_top"] = self.df["locality_name"].where(self.df["locality_name"].isin(top_localities), "other")
            cat_locality = pd.get_dummies(self.df["locality_top"], prefix="loc", drop_first=True)
            self.df = pd.concat([self.df, cat_locality], axis=1)
            loc_cols = cat_locality.columns.tolist()
            print(f"  ✓ Created {len(loc_cols)} locality features")
        
        # Area category dummies
        area_cat_dummies = pd.get_dummies(self.df["area_cat"], prefix="area_cat", drop_first=True)
        self.df = pd.concat([self.df, area_cat_dummies], axis=1)
        
        # City dummies
        city_cols = []
        if "city_name" in self.df.columns:
            top_cities = self.df["city_name"].value_counts().nlargest(10).index
            self.df["city_top"] = self.df["city_name"].where(self.df["city_name"].isin(top_cities), "other")
            city_dummies = pd.get_dummies(self.df["city_top"], prefix="city", drop_first=True)
            self.df = pd.concat([self.df, city_dummies], axis=1)
            city_cols = city_dummies.columns.tolist()
            print(f"  ✓ Created {len(city_cols)} city features")
        
        self.features = base_feats + loc_cols + city_cols + area_cat_dummies.columns.tolist()
        self.features = [c for c in self.features if c in self.df.columns]
        print(f"✓ Final feature count: {len(self.features)}")
        
        return self
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into train/test sets"""
        print(f"📊 Splitting data ({test_size*100}% test)...")
        
        X = self.df[self.features].fillna(0)
        y = self.df["price_num"]
        
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(self.X_train)
        X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✓ Train: {self.X_train.shape}, Test: {self.X_test.shape}")
        
        return self
    
    def train_baseline_models(self):
        """Train baseline models"""
        print("\n🤖 Training baseline models...")
        
        self.lr = Ridge(alpha=1.0)
        self.rf = RandomForestRegressor(n_estimators=20, max_depth=10, n_jobs=-1, random_state=42)
        self.lgb = LGBMRegressor(n_estimators=50, learning_rate=0.1, n_jobs=-1, random_state=42, verbose=-1)
        self.xgb = XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=5, n_jobs=-1, tree_method='hist', random_state=42, verbosity=0)
        
        X_train_scaled = self.scaler.fit_transform(self.X_train)
        
        print("  Fitting Ridge...")
        self.lr.fit(X_train_scaled, self.y_train)
        
        print("  Fitting Random Forest...")
        self.rf.fit(self.X_train, self.y_train)
        
        print("  Fitting LightGBM...")
        self.lgb.fit(self.X_train, self.y_train, eval_set=[(self.X_test, self.y_test)])
        
        print("  Fitting XGBoost...")
        self.xgb.fit(self.X_train, self.y_train, eval_set=[(self.X_test, self.y_test)], verbose=False)
        
        print("✓ All baseline models trained!")
        return self
    
    def evaluate_models(self):
        """Evaluate baseline models"""
        def eval_preds(name, y_true, y_pred):
            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            r2 = r2_score(y_true, y_pred)
            print(f"  {name}: MAE={mae:,.0f}, RMSE={rmse:,.0f}, R2={r2:.4f}")
            return {"mae": mae, "rmse": rmse, "r2": r2}
        
        print("\n" + "=" * 60)
        print("📊 BASELINE MODEL RESULTS")
        print("=" * 60)
        
        X_test_scaled = self.scaler.transform(self.X_test)
        eval_preds("Ridge", self.y_test, self.lr.predict(X_test_scaled))
        eval_preds("RandomForest", self.y_test, self.rf.predict(self.X_test))
        eval_preds("LightGBM", self.y_test, self.lgb.predict(self.X_test))
        eval_preds("XGBoost", self.y_test, self.xgb.predict(self.X_test))
        print("=" * 60)
        
        return self
    
    def train_stacking_ensemble(self):
        """Train stacking ensemble model"""
        print("\n🎯 Training Stacking Ensemble...")
        
        estimators = [
            ('rf', RandomForestRegressor(n_estimators=20, max_depth=10, n_jobs=-1, random_state=42)),
            ('lgb', LGBMRegressor(n_estimators=50, learning_rate=0.1, n_jobs=-1, random_state=42, verbose=-1)),
            ('xgb', XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=5, n_jobs=-1, tree_method='hist', random_state=42, verbosity=0))
        ]
        
        final_estimator = Ridge(alpha=1.0)
        self.stacking_regressor = StackingRegressor(estimators=estimators, final_estimator=final_estimator, cv=3)
        
        print("  Fitting ensemble (may take a few minutes)...")
        self.stacking_regressor.fit(self.X_train, self.y_train)
        
        print("✓ Stacking ensemble trained!")
        
        # Evaluate
        y_pred = self.stacking_regressor.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        r2 = r2_score(self.y_test, y_pred)
        print(f"\n  Ensemble: MAE={mae:,.0f}, RMSE={rmse:,.0f}, R2={r2:.4f}")
        
        return self
    
    def save_model(self):
        """Save trained model and artifacts"""
        print("\n💾 Saving model...")
        
        pipeline_path = os.path.join(self.project_root, "backend/models/pipeline_v1.pkl")
        os.makedirs(os.path.dirname(pipeline_path), exist_ok=True)
        
        joblib.dump(self.stacking_regressor, pipeline_path)
        print(f"✓ Model saved to: {pipeline_path}")
        
        joblib.dump(self.scaler, os.path.join(self.project_root, "backend/models/scaler.pkl"))
        joblib.dump(self.features, os.path.join(self.project_root, "backend/models/features.pkl"))
        print("✓ Scaler and features saved")
        
        return self
    
    def print_feature_importance(self, top_n=15):
        """Print top features by importance"""
        print(f"\n📈 Top {top_n} Features (LightGBM):")
        imp = pd.Series(self.lgb.feature_importances_, index=self.X_train.columns).sort_values(ascending=False)
        print(imp.head(top_n))
        
        return self
    
    def run_full_pipeline(self, cleaned_file):
        """Run the complete pipeline"""
        print("=" * 60)
        print("🚀 REAL ESTATE ML PIPELINE")
        print("=" * 60 + "\n")
        
        return (self
                .load_data(cleaned_file)
                .validate_data()
                .engineer_features()
                .prepare_features()
                .split_data()
                .train_baseline_models()
                .evaluate_models()
                .train_stacking_ensemble()
                .print_feature_importance()
                .save_model())


if __name__ == "__main__":
    # Setup paths
    project_root = r"C:\Users\SOUMIK\Downloads\infosys_internship-main\infosys_internship-main"
    cleaned_file = os.path.join(project_root, "cleaned_indian_property.csv")
    
    # Initialize and run pipeline
    pipeline = RealEstatePipeline(project_root)
    pipeline.run_full_pipeline(cleaned_file)
    
    print("\n✨ Training complete! Pipeline ready for deployment.")
