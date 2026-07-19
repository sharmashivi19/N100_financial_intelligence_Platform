# Day 03 Schema Validator

Implemented DQ rules:

- DQ-01 Missing Primary Key
- DQ-02 Duplicate Primary Key
- DQ-03 Missing Required Columns
- DQ-04 Invalid Foreign Key
- DQ-05 Invalid Datatype
- DQ-06 Duplicate Records
- DQ-07 Invalid Ticker
- DQ-08 Invalid Year
- DQ-09 Missing Company Data
- DQ-10 Negative Sales
- DQ-11 Incorrect OPM
- DQ-12 Balance Validation
- DQ-13 Profit Calculation
- DQ-14 Financial Period Check
- DQ-15 Currency Validation
- DQ-16 Outlier Detection

Output:
validation_failures.csv
# N100 Financial Intelligence Platform

A financial analytics dashboard built using Python, Streamlit, SQLite, Pandas and Plotly.

---

# Features

This project provides financial analysis for Nifty 100 companies including:

- Company Profile
- Financial Statements
- Stock Screener
- Trend Analysis
- Sector Analysis
- Peer Comparison
- Capital Allocation
- Financial Report

---

# Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- OpenPyXL

---

# Project Structure

```
N100_Financial_Intelligence_Platform/

│
├── database/
│       nifty100.db
│
├── data/
│       source_files/
│
├── output/
│
├── src/
│   ├── analytics/
│   └── dashboard/
│        ├── app.py
│        └── pages/
│
├── README.md
```

---

# Installation

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Install Packages

```bash
pip install -r requirements.txt
```

---

# Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

Dashboard will open at

```
http://localhost:8501
```

---

# Data Source

The dashboard uses

- SQLite Database
- Excel Source Files

Located inside

```
database/
data/source_files/
```

---

# Output Files

Generated outputs are stored in

```
output/
```

Examples

- valuation_summary.xlsx
- valuation_flags.csv

---

# Dashboard Screens

## 1. Company Profile

Displays company overview including:

- About Company
- ROE
- ROCE
- Website
- Company Information

Screenshot:

(Add Screenshot Here)

---

## 2. Financial Statements

Displays

- Profit & Loss
- Balance Sheet
- Cash Flow

Screenshot:

(Add Screenshot Here)

---

## 3. Stock Screener

Allows filtering companies using

- ROE
- Debt
- Revenue CAGR
- PAT CAGR
- EPS CAGR

Screenshot:

(Add Screenshot Here)

---

## 4. Trend Analysis

Interactive line charts showing

- ROE
- OPM
- Revenue CAGR
- PAT CAGR

Screenshot:

(Add Screenshot Here)

---

## 5. Sector Analysis

Shows

- Sector Median KPIs
- Bubble Chart
- Company List

Screenshot:

(Add Screenshot Here)

---

## 6. Peer Comparison

Compare companies inside peer groups.

Shows

- ROE
- OPM
- Debt
- Composite Score

Screenshot:

(Add Screenshot Here)

---

## 7. Capital Allocation

Displays

- Free Cash Flow
- Capex
- Debt
- Cash From Operations

Screenshot:

(Add Screenshot Here)

---

## 8. Financial Report

Generate downloadable reports for selected companies.

Screenshot:

(Add Screenshot Here)

# Sprint 4 Retrospective

## UX Decisions

- Added sidebar filters for quick stock screening.
- Used Plotly interactive charts.
- Added download buttons for CSV reports.
- Used dropdown selectors for companies and sectors.

---

## Data Edge Cases

Handled

- Missing financial years
- Missing ratios
- Missing market capitalization
- Duplicate rows
- Companies with fewer financial records

Displayed N/A instead of crashing whenever data was unavailable.

---

## Performance Findings

- Dashboard loads within approximately 2–3 seconds.
- SQLite queries execute quickly for 92 companies.
- Plotly charts render smoothly.
- Streamlit page transitions are responsive.

---

## Bugs Fixed

- Database schema mismatch
- Year datatype mismatch
- Duplicate merge columns
- Missing company names
- Plotly width issues
- Merge conflicts

# Sprint 4 Task Status

| Module | Status |
|---------|--------|
| Company Profile | ✅ Completed |
| Financial Statements | ✅ Completed |
| Stock Screener | ✅ Completed |
| Trend Analysis | ✅ Completed |
| Sector Analysis | ✅ Completed |
| Peer Comparison | ✅ Completed |
| Capital Allocation | ✅ Completed |
| Financial Report | ✅ Completed |
| Valuation Module | ✅ Completed |
| Integration Testing | ✅ Completed |
| Documentation | ✅ Completed |
![Company Profile](docs/screenshots/company_profile.png)
![Financials](docs/screenshots/financials.png)
![Screener](docs/screenshots/screener.png)     
![trend](docs/screenshots/trend.png)
![Sector](docs/screenshots/sector.png)
![peer](docs/screenshots/peer.png)
![capital](docs/screenshots/capital.png)
![report](docs/screenshots/report.png)