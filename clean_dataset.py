import pandas as pd
import numpy as np
import os
import sys

print("=" * 60)
print("🏡 Real Estate Dataset Cleaning Pipeline")
print("=" * 60)

# 1. Load dataset
csv_file = "Makaan_Properties_Buy.csv"
if not os.path.exists(csv_file):
    print(f"❌ Error: {csv_file} not found in current directory.")
    print(f"   Current directory: {os.getcwd()}")
    sys.exit(1)

try:
    df = pd.read_csv(csv_file, encoding='latin1')
except Exception as e:
    print(f"❌ Error reading {csv_file}: {e}")
    sys.exit(1)

# 2. Inspect
print(f"\n📊 Initial dataset shape: {df.shape}")
print(f"\nFirst 5 rows:")
print(df.head())
print(f"\nData types and missing values:")
print(df.info())
print(f"\nMissing value counts (top 15):")
print(df.isnull().sum().sort_values(ascending=False).head(15))

# 3. Drop columns with >25% missing
print("\n🗑️  Step 3: Dropping columns with >25% missing values...")
threshold = 0.25
cols_to_drop = df.columns[df.isnull().mean() > threshold]
if len(cols_to_drop) > 0:
    print(f"   Dropped {len(cols_to_drop)} columns: {list(cols_to_drop)}")
    df = df.drop(columns=cols_to_drop)
else:
    print("   No columns with >25% missing values found.")

# 4. Drop rows with nulls in essential fields
print("\n🔍 Step 4: Dropping rows with missing essential fields...")
essential = ["Price", "Size", "City_name"]
missing_essential = df[essential].isnull().sum()
print(f"   Missing values before drop: {dict(missing_essential)}")
df_before = len(df)
df = df.dropna(subset=essential)
print(f"   Dropped {df_before - len(df)} rows with missing essential fields.")
print(f"   Shape after: {df.shape}")

# 5. Convert price strings to numbers
print("\n💰 Step 5: Converting price strings to numeric values...")

def parse_price(x):
    """Convert price strings (e.g., '50 Cr', '5 Lakh') to float."""
    try:
        x = str(x).strip()
        if not x or x.lower() == 'nan':
            return np.nan
        if 'Cr' in x:
            return float(x.replace('Cr','').replace(',','').strip()) * 1e7
        elif 'Lac' in x or 'Lakh' in x or 'Lacs' in x:
            return float(x.replace('Lac','').replace('Lakh','').replace('Lacs','').replace(',','').strip()) * 1e5
        else:
            return float(x.replace(',','').strip())
    except Exception as e:
        return np.nan

df['price_num'] = df['Price'].apply(parse_price)
price_success = df['price_num'].notna().sum()
print(f"   Successfully converted {price_success}/{len(df)} prices.")
print(f"   Price range: ₹{df['price_num'].min():.0f} - ₹{df['price_num'].max():.0f}")

# 6. Convert area to numbers
print("\n📐 Step 6: Converting area strings to numeric values...")

def parse_area(x):
    """Extract numeric value from area strings (e.g., '1,200 sq.ft')."""
    try:
        s = str(x).strip()
        if not s or s.lower() == 'nan':
            return np.nan
        num = ''.join(ch for ch in s if ch.isdigit() or ch in ['.', ','])
        if not num:
            return np.nan
        return float(num.replace(',',''))
    except Exception as e:
        return np.nan

df['area_num'] = df['Size'].apply(parse_area)
area_success = df['area_num'].notna().sum()
print(f"   Successfully converted {area_success}/{len(df)} areas.")
if area_success > 0:
    print(f"   Area range: {df['area_num'].min():.0f} - {df['area_num'].max():.0f} sq.ft")

# 7. Drop rows where conversion failed
print("\n🧹 Step 7: Removing rows with invalid price or area...")
df_before = len(df)
df = df[df['price_num'].notna() & df['area_num'].notna()]
df = df[df['price_num'] > 0]  # Price must be positive
df = df[df['area_num'] > 0]   # Area must be positive
print(f"   Removed {df_before - len(df)} invalid rows.")
print(f"   Shape after: {df.shape}")

# 8. Drop duplicates
print("\n🔄 Step 8: Removing duplicate rows...")
df_before = len(df)
df = df.drop_duplicates()
print(f"   Removed {df_before - len(df)} duplicate rows.")
print(f"   Shape after: {df.shape}")

# 9. Handle outliers (remove top & bottom 1%)
print("\n📊 Step 9: Handling outliers (removing bottom/top 1%)...")
for col in ['price_num', 'area_num']:
    q_low, q_high = df[col].quantile([0.01, 0.99])
    df_before = len(df)
    df = df[(df[col] >= q_low) & (df[col] <= q_high)]
    print(f"   {col}: removed {df_before - len(df)} outliers (1%-99% range)")
print(f"   Shape after outlier removal: {df.shape}")

# 10. Feature engineering
print("\n⚙️  Step 10: Engineering features...")
df['price_per_sqft'] = df['price_num'] / df['area_num']
print(f"   Created 'price_per_sqft' feature")
print(f"   Price/sqft range: ₹{df['price_per_sqft'].min():.0f} - ₹{df['price_per_sqft'].max():.0f}/sqft")

# 11. Final validation and save
print("\n✅ Step 11: Final validation and saving...")
print(f"   Final dataset shape: {df.shape}")
print(f"   Columns: {list(df.columns)}")
print(f"\n   Sample statistics:")
print(df[['price_num', 'area_num', 'price_per_sqft']].describe().round(2))

output_file = "cleaned_indian_property.csv"
try:
    df.to_csv(output_file, index=False)
    print(f"\n✓ Cleaned dataset saved to: {output_file}")
    print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
except Exception as e:
    print(f"\n❌ Error saving file: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ Data cleaning pipeline completed successfully!")
print("=" * 60)

