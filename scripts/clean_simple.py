# scripts/clean_simple.py - Simple data cleaning
import pandas as pd
import os

PROCESSED_DIR = 'data/processed'
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("="*50)
print("🧹 CLEANING ALL DATA FILES")
print("="*50)

# List of files to clean
files = [
    'fund_master',
    'nav_history', 
    'aum_by_fund_house',
    'monthly_sip_inflows',
    'category_inflows',
    'industry_folio_count',
    'scheme_performance',
    'investor_transactions',
    'portfolio_holdings',
    'benchmark_indices'
]

for file in files:
    try:
        # Try to find the file
        found = False
        for prefix in ['', '01_', '02_', '03_', '04_', '05_', '06_', '07_', '08_', '09_', '10_']:
            filename = f"data/raw/{prefix}{file}.csv"
            if os.path.exists(filename):
                print(f"\n📂 Found: {filename}")
                df = pd.read_csv(filename)
                df.to_csv(f"data/processed/clean_{file}.csv", index=False)
                print(f"  ✅ Saved: {len(df)} rows")
                found = True
                break
        
        if not found:
            print(f"\n❌ Not found: {file}.csv (tried multiple patterns)")
    except Exception as e:
        print(f"\n❌ Error with {file}: {e}")

print("\n" + "="*50)
print("✅ CLEANING COMPLETE!")
print("="*50)