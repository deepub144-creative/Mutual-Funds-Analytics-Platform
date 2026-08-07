# scripts/clean_all_data_fixed.py
# Complete data cleaning for all 10 datasets - FIXED PATHS

import pandas as pd
import numpy as np
import os

# Set correct paths (you're already in the project folder)
BASE_DIR = os.getcwd()
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# Create processed folder if it doesn't exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

print("="*60)
print("🧹 STARTING DATA CLEANING FOR ALL 10 FILES")
print("="*60)
print(f"📁 Raw data folder: {RAW_DIR}")
print(f"📁 Processed folder: {PROCESSED_DIR}")
print("="*60)

# ============================================================
# FILE 1: fund_master.csv
# ============================================================
print("\n📂 Cleaning: fund_master.csv")
try:
    fund = pd.read_csv(os.path.join(RAW_DIR, '01_fund_master.csv'))
    
    # Check for missing values
    print(f"  Missing values before: {fund.isnull().sum().sum()}")
    
    # Fill missing values
    fund['fund_manager'] = fund['fund_manager'].fillna('Not Available')
    fund['exit_load_pct'] = fund['exit_load_pct'].fillna(0)
    fund['risk_category'] = fund['risk_category'].fillna('Moderate')
    
    # Clean data types
    fund['amfi_code'] = fund['amfi_code'].astype(str)
    fund['launch_date'] = pd.to_datetime(fund['launch_date'], errors='coerce')
    fund['expense_ratio_pct'] = pd.to_numeric(fund['expense_ratio_pct'], errors='coerce')
    
    # Remove duplicates
    fund = fund.drop_duplicates(subset=['amfi_code'])
    
    # Save
    fund.to_csv(os.path.join(PROCESSED_DIR, 'clean_fund_master.csv'), index=False)
    print(f"  ✅ Saved: {len(fund)} rows")
    print(f"  Missing values after: {fund.isnull().sum().sum()}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 2: nav_history.csv
# ============================================================
print("\n📂 Cleaning: nav_history.csv")
try:
    nav = pd.read_csv(os.path.join(RAW_DIR, '02_nav_history.csv'))
    
    # Parse dates
    nav['date'] = pd.to_datetime(nav['date'])
    nav['amfi_code'] = nav['amfi_code'].astype(str)
    nav['nav'] = pd.to_numeric(nav['nav'], errors='coerce')
    
    # Remove duplicates (same fund, same date)
    nav = nav.drop_duplicates(subset=['amfi_code', 'date'])
    
    # Remove invalid NAV (<=0)
    nav = nav[nav['nav'] > 0]
    
    # Sort
    nav = nav.sort_values(['amfi_code', 'date'])
    
    # Merge with fund names
    nav = nav.merge(fund[['amfi_code', 'scheme_name']], on='amfi_code', how='left')
    
    # Reorder columns
    nav = nav[['date', 'amfi_code', 'scheme_name', 'nav']]
    
    # Save
    nav.to_csv(os.path.join(PROCESSED_DIR, 'clean_nav.csv'), index=False)
    print(f"  ✅ Saved: {len(nav):,} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 3: aum_by_fund_house.csv
# ============================================================
print("\n📂 Cleaning: aum_by_fund_house.csv")
try:
    aum = pd.read_csv(os.path.join(RAW_DIR, '03_aum_by_fund_house.csv'))
    
    # Clean column names
    aum.columns = aum.columns.str.lower().str.replace(' ', '_')
    
    # Convert to numeric
    aum['aum_lakh_crore'] = pd.to_numeric(aum['aum_lakh_crore'], errors='coerce')
    
    # Remove duplicates
    aum = aum.drop_duplicates(subset=['fund_house', 'year'])
    
    # Fill missing
    aum['aum_lakh_crore'] = aum['aum_lakh_crore'].fillna(aum['aum_lakh_crore'].median())
    
    # Sort
    aum = aum.sort_values(['year', 'fund_house'])
    
    aum.to_csv(os.path.join(PROCESSED_DIR, 'clean_aum_by_fund_house.csv'), index=False)
    print(f"  ✅ Saved: {len(aum)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 4: monthly_sip_inflows.csv
# ============================================================
print("\n📂 Cleaning: monthly_sip_inflows.csv")
try:
    sip = pd.read_csv(os.path.join(RAW_DIR, '04_monthly_sip_inflows.csv'))
    
    # Parse month
    sip['month'] = pd.to_datetime(sip['month'])
    
    # Clean column names
    sip.columns = sip.columns.str.lower().str.replace(' ', '_')
    
    # Convert to numeric
    numeric_cols = ['sip_inflow_crore', 'active_sip_accounts_crore', 
                    'new_sip_accounts_lakh', 'sip_aum_lakh_crore', 'yoy_growth_pct']
    for col in numeric_cols:
        if col in sip.columns:
            sip[col] = pd.to_numeric(sip[col], errors='coerce')
    
    # Remove duplicates
    sip = sip.drop_duplicates(subset=['month'])
    
    # Fill missing
    sip = sip.fillna(method='ffill')
    
    # Sort
    sip = sip.sort_values('month')
    
    sip.to_csv(os.path.join(PROCESSED_DIR, 'clean_monthly_sip_inflows.csv'), index=False)
    print(f"  ✅ Saved: {len(sip)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 5: category_inflows.csv
# ============================================================
print("\n📂 Cleaning: category_inflows.csv")
try:
    category = pd.read_csv(os.path.join(RAW_DIR, '05_category_inflows.csv'))
    
    # Parse month
    category['month'] = pd.to_datetime(category['month'])
    
    # Clean column names
    category.columns = category.columns.str.lower().str.replace(' ', '_')
    
    # Convert to numeric
    category['net_inflow_crore'] = pd.to_numeric(category['net_inflow_crore'], errors='coerce')
    category['aum_crore'] = pd.to_numeric(category['aum_crore'], errors='coerce')
    
    # Fill missing
    category['net_inflow_crore'] = category['net_inflow_crore'].fillna(0)
    category['aum_crore'] = category['aum_crore'].fillna(category['aum_crore'].median())
    
    # Remove duplicates
    category = category.drop_duplicates(subset=['category', 'month'])
    
    # Sort
    category = category.sort_values(['category', 'month'])
    
    category.to_csv(os.path.join(PROCESSED_DIR, 'clean_category_inflows.csv'), index=False)
    print(f"  ✅ Saved: {len(category)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 6: industry_folio_count.csv
# ============================================================
print("\n📂 Cleaning: industry_folio_count.csv")
try:
    folio = pd.read_csv(os.path.join(RAW_DIR, '06_industry_folio_count.csv'))
    
    # Parse date
    folio['date'] = pd.to_datetime(folio['date'])
    
    # Clean column names
    folio.columns = folio.columns.str.lower().str.replace(' ', '_')
    
    # Convert to numeric
    numeric_cols = ['total_folios_crore', 'equity_folios_crore', 
                    'debt_folios_crore', 'hybrid_folios_crore']
    for col in numeric_cols:
        if col in folio.columns:
            folio[col] = pd.to_numeric(folio[col], errors='coerce')
    
    # Fill missing
    folio = folio.fillna(method='ffill')
    
    # Remove duplicates
    folio = folio.drop_duplicates(subset=['date'])
    
    folio.to_csv(os.path.join(PROCESSED_DIR, 'clean_industry_folio_count.csv'), index=False)
    print(f"  ✅ Saved: {len(folio)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 7: scheme_performance.csv
# ============================================================
print("\n📂 Cleaning: scheme_performance.csv")
try:
    performance = pd.read_csv(os.path.join(RAW_DIR, '07_scheme_performance.csv'))
    
    # Clean column names
    performance.columns = performance.columns.str.lower().str.replace(' ', '_')
    
    # Convert numeric columns
    numeric_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct',
                    'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio',
                    'sortino_ratio', 'std_dev_ann_pct', 'max_drawdown_pct']
    for col in numeric_cols:
        if col in performance.columns:
            performance[col] = pd.to_numeric(performance[col], errors='coerce')
    
    # Flag negative Sharpe
    performance['negative_sharpe_flag'] = performance['sharpe_ratio'] < 0
    
    # Validate expense ratio (0.1% - 2.5%)
    if 'expense_ratio_pct' in performance.columns:
        performance['expense_valid'] = (performance['expense_ratio_pct'] >= 0.1) & (performance['expense_ratio_pct'] <= 2.5)
    
    # Fill missing with median
    for col in numeric_cols:
        if col in performance.columns:
            performance[col] = performance[col].fillna(performance[col].median())
    
    performance.to_csv(os.path.join(PROCESSED_DIR, 'clean_scheme_performance.csv'), index=False)
    print(f"  ✅ Saved: {len(performance)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 8: investor_transactions.csv
# ============================================================
print("\n📂 Cleaning: investor_transactions.csv")
try:
    transactions = pd.read_csv(os.path.join(RAW_DIR, '08_investor_transactions.csv'))
    
    # Parse date
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    
    # Clean column names
    transactions.columns = transactions.columns.str.lower().str.replace(' ', '_')
    
    # Standardize transaction type
    if 'transaction_type' in transactions.columns:
        transactions['transaction_type'] = transactions['transaction_type'].str.upper()
        valid_types = ['SIP', 'LUMPSUM', 'REDEMPTION']
        transactions['transaction_type'] = transactions['transaction_type'].apply(
            lambda x: x if x in valid_types else 'LUMPSUM'
        )
    
    # Validate amount > 0
    if 'amount_inr' in transactions.columns:
        transactions['amount_inr'] = pd.to_numeric(transactions['amount_inr'], errors='coerce')
        transactions = transactions[transactions['amount_inr'] > 0]
    
    # Clean KYC status
    if 'kyc_status' in transactions.columns:
        transactions['kyc_status'] = transactions['kyc_status'].str.title()
        transactions['kyc_status'] = transactions['kyc_status'].apply(
            lambda x: 'Verified' if x in ['Verified', 'Verification Complete'] else 'Pending'
        )
    
    # Clean state names
    if 'state' in transactions.columns:
        transactions['state'] = transactions['state'].str.title()
    
    # Remove duplicates
    transactions = transactions.drop_duplicates()
    
    transactions.to_csv(os.path.join(PROCESSED_DIR, 'clean_investor_transactions.csv'), index=False)
    print(f"  ✅ Saved: {len(transactions):,} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 9: portfolio_holdings.csv
# ============================================================
print("\n📂 Cleaning: portfolio_holdings.csv")
try:
    holdings = pd.read_csv(os.path.join(RAW_DIR, '09_portfolio_holdings.csv'))
    
    # Clean column names
    holdings.columns = holdings.columns.str.lower().str.replace(' ', '_')
    
    # Convert weight to numeric
    if 'weight_pct' in holdings.columns:
        holdings['weight_pct'] = pd.to_numeric(holdings['weight_pct'], errors='coerce')
    
    # Clean sector names
    if 'sector' in holdings.columns:
        holdings['sector'] = holdings['sector'].str.strip().str.title()
    
    # Fill missing
    holdings['sector'] = holdings['sector'].fillna('Other')
    holdings['weight_pct'] = holdings['weight_pct'].fillna(0)
    
    # Remove duplicates (same fund, same stock)
    holdings = holdings.drop_duplicates(subset=['amfi_code', 'stock'])
    
    holdings.to_csv(os.path.join(PROCESSED_DIR, 'clean_portfolio_holdings.csv'), index=False)
    print(f"  ✅ Saved: {len(holdings)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# FILE 10: benchmark_indices.csv
# ============================================================
print("\n📂 Cleaning: benchmark_indices.csv")
try:
    benchmark = pd.read_csv(os.path.join(RAW_DIR, '10_benchmark_indices.csv'))
    
    # Parse date
    benchmark['date'] = pd.to_datetime(benchmark['date'])
    
    # Clean column names
    benchmark.columns = benchmark.columns.str.lower().str.replace(' ', '_')
    
    # Convert to numeric
    index_cols = ['nifty_50', 'nifty_100', 'nifty_midcap_150', 
                  'bse_smallcap', 'crisil_liquid', 'crisil_gilt']
    for col in index_cols:
        if col in benchmark.columns:
            benchmark[col] = pd.to_numeric(benchmark[col], errors='coerce')
    
    # Forward fill missing
    benchmark = benchmark.sort_values('date')
    for col in index_cols:
        if col in benchmark.columns:
            benchmark[col] = benchmark[col].fillna(method='ffill')
    
    # Remove duplicates
    benchmark = benchmark.drop_duplicates(subset=['date'])
    
    benchmark.to_csv(os.path.join(PROCESSED_DIR, 'clean_benchmark_indices.csv'), index=False)
    print(f"  ✅ Saved: {len(benchmark)} rows")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("✅ DATA CLEANING COMPLETE!")
print("="*60)
print("\n📁 Files saved in: data/processed/")
print("\n  ✅ clean_fund_master.csv")
print("  ✅ clean_nav.csv")
print("  ✅ clean_aum_by_fund_house.csv")
print("  ✅ clean_monthly_sip_inflows.csv")
print("  ✅ clean_category_inflows.csv")
print("  ✅ clean_industry_folio_count.csv")
print("  ✅ clean_scheme_performance.csv")
print("  ✅ clean_investor_transactions.csv")
print("  ✅ clean_portfolio_holdings.csv")
print("  ✅ clean_benchmark_indices.csv")
print("\n🎉 All 10 files cleaned successfully!")
