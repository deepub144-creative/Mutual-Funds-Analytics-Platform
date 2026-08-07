# Data Dictionary — Bluestock Mutual Fund Analytics

## dim_fund
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (PK) | Unique fund identifier | scheme_performance.csv |
| scheme_name | TEXT | Name of the mutual fund scheme | scheme_performance.csv |
| fund_house | TEXT | AMC managing the fund | scheme_performance.csv |
| category | TEXT | Fund category (e.g. Large Cap, Small Cap) | scheme_performance.csv |
| plan | TEXT | Regular or Direct plan | scheme_performance.csv |
| morningstar_rating | INTEGER | Star rating (1–5) | scheme_performance.csv |
| risk_grade | TEXT | Risk level (Low/Moderate/High/Very High) | scheme_performance.csv |

## fact_nav
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (FK) | Links to dim_fund | nav_history.csv |
| nav_date | DATE | Date of NAV record | nav_history.csv |
| nav | REAL | Net Asset Value on that date | nav_history.csv |
| daily_return | REAL | Day-over-day return % | calculated |

## fact_transactions
| Column | Type | Description | Source |
|---|---|---|---|
| investor_id | TEXT | Unique investor identifier | investor_transactions.csv |
| transaction_date | DATE | Date of transaction | investor_transactions.csv |
| amfi_code | TEXT (FK) | Fund invested in | investor_transactions.csv |
| transaction_type | TEXT | SIP / Lumpsum / Redemption | investor_transactions.csv |
| amount_inr | REAL | Transaction amount in INR | investor_transactions.csv |
| state | TEXT | Investor's state | investor_transactions.csv |
| city | TEXT | Investor's city | investor_transactions.csv |
| city_tier | TEXT | City tier (T30/B30) | investor_transactions.csv |
| age_group | TEXT | Investor age bracket | investor_transactions.csv |
| gender | TEXT | Investor gender | investor_transactions.csv |
| annual_income_lakh | REAL | Annual income (in lakhs) | investor_transactions.csv |
| payment_mode | TEXT | UPI/Cheque/Mandate etc. | investor_transactions.csv |
| kyc_status | TEXT | Verified/Pending/Rejected | investor_transactions.csv |

## fact_performance
| Column | Type | Description | Source |
|---|---|---|---|
| amfi_code | TEXT (FK) | Links to dim_fund | scheme_performance.csv |
| return_1yr_pct | REAL | 1-year return % | scheme_performance.csv |
| return_3yr_pct | REAL | 3-year return % | scheme_performance.csv |
| return_5yr_pct | REAL | 5-year return % | scheme_performance.csv |
| benchmark_3yr_pct | REAL | Benchmark 3-year return % | scheme_performance.csv |
| alpha | REAL | Alpha (excess return vs benchmark) | scheme_performance.csv |
| beta | REAL | Beta (volatility vs market) | scheme_performance.csv |
| sharpe_ratio | REAL | Risk-adjusted return metric | scheme_performance.csv |
| sortino_ratio | REAL | Downside risk-adjusted return | scheme_performance.csv |
| std_dev_ann_pct | REAL | Annualized standard deviation | scheme_performance.csv |
| max_drawdown_pct | REAL | Maximum historical drop % | scheme_performance.csv |
| aum_crore | REAL | Assets under management (₹ crore) | scheme_performance.csv |
| expense_ratio_pct | REAL | Fund expense ratio % | scheme_performance.csv |