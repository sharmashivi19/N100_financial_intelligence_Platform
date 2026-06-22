PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS companies (

    company_id INTEGER PRIMARY KEY,
    ticker TEXT UNIQUE NOT NULL,
    company_name TEXT NOT NULL,
    sector TEXT

);


CREATE TABLE IF NOT EXISTS financials (

    financial_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    sales REAL,
    operating_profit REAL,
    opm REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS balance_sheet (

    balance_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    year INTEGER,
    assets REAL,
    liabilities REAL,
    equity REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS income_statement (

    income_id INTEGER PRIMARY KEY,
    company_id INTEGER NOT NULL,
    revenue REAL,
    expense REAL,
    profit REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS stock_prices (

    price_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    date TEXT,
    close_price REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS dividends (

    dividend_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    dividend REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS shareholding (

    holding_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    promoter REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS ratios (

    ratio_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    pe_ratio REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS market_cap (

    marketcap_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    market_cap REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);


CREATE TABLE IF NOT EXISTS financial_period (

    period_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    period TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)

);