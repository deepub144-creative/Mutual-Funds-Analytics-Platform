import pandas as pd
import sqlite3
from pathlib import Path
import os

# ---------- Configuration ----------
# Use the current working directory as base
BASE_DIR = Path.cwd()
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "db" / "bluestock_mf.db"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# ---------- Map your actual file names to table names ----------
files = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum_by_fund_house": "03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "scheme_performance": "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings": "09_portfolio_holdings.csv",
    "benchmark_indices": "10_benchmark_indices.csv",
}

dataframes = {}

for name, fname in files.items():
    path = RAW_DIR / fname
    if path.exists():
        print(f"Loading {name} from {fname}...")
        df = pd.read_csv(path)
        print(f"  -> {df.shape[0]} rows, {df.shape[1]} columns")
        dataframes[name] = df
    else:
        print(f"⚠️ File not found: {fname}")

# ---------- Basic Cleaning ----------
if "fund_master" in dataframes:
    fm = dataframes["fund_master"]
    if "amfi_code" in fm.columns:
        fm["amfi_code"] = pd.to_numeric(fm["amfi_code"], errors="coerce").astype("Int64")
    dataframes["fund_master"] = fm

if "nav_history" in dataframes:
    nav = dataframes["nav_history"]
    if "date" in nav.columns:
        nav["date"] = pd.to_datetime(nav["date"])
    if "nav" in nav.columns:
        nav["nav"] = pd.to_numeric(nav["nav"], errors="coerce")
    dataframes["nav_history"] = nav

if "aum_by_fund_house" in dataframes:
    aum = dataframes["aum_by_fund_house"]
    if "date" in aum.columns:
        aum["date"] = pd.to_datetime(aum["date"])
    dataframes["aum_by_fund_house"] = aum

if "investor_transactions" in dataframes:
    it = dataframes["investor_transactions"]
    if "transaction_date" in it.columns:
        it["transaction_date"] = pd.to_datetime(it["transaction_date"])
    if "amount_inr" in it.columns:
        it["amount_inr"] = pd.to_numeric(it["amount_inr"], errors="coerce")
    dataframes["investor_transactions"] = it

if "category_inflows" in dataframes:
    ci = dataframes["category_inflows"]
    if "month" in ci.columns:
        ci["month"] = pd.to_datetime(ci["month"])
    dataframes["category_inflows"] = ci

if "benchmark_indices" in dataframes:
    bi = dataframes["benchmark_indices"]
    if "date" in bi.columns:
        bi["date"] = pd.to_datetime(bi["date"])
    dataframes["benchmark_indices"] = bi

if "industry_folio_count" in dataframes:
    ifc = dataframes["industry_folio_count"]
    if "month" in ifc.columns:
        ifc["month"] = pd.to_datetime(ifc["month"])
    dataframes["industry_folio_count"] = ifc

# ---------- Save cleaned copies (optional) ----------
for name, df in dataframes.items():
    if df is not None:
        df.to_csv(PROCESSED_DIR / f"{name}_cleaned.csv", index=False)

# ---------- Load into SQLite ----------
conn = sqlite3.connect(DB_PATH)
for name, df in dataframes.items():
    if df is not None and len(df) > 0:
        df.to_sql(name, conn, if_exists="replace", index=False)
        print(f"✅ Table '{name}' created with {len(df)} rows.")
conn.close()

print(f"\n✅ Database saved to {DB_PATH}")
