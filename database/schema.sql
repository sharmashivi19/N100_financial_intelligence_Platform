PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS companies (

    id TEXT PRIMARY KEY,

    company_logo TEXT,

    company_name TEXT NOT NULL,

    chart_link TEXT,

    about_company TEXT,

    website TEXT,

    nse_profile TEXT,

    bse_profile TEXT,

    face_value REAL,

    book_value REAL,

    roce_percentage REAL,

    roe_percentage REAL

);

CREATE TABLE IF NOT EXISTS financials (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year TEXT,

    sales REAL,

    expenses REAL,

    operating_profit REAL,

    opm_percentage REAL,

    other_income REAL,

    interest REAL,

    depreciation REAL,

    profit_before_tax REAL,

    tax_percentage REAL,

    net_profit REAL,

    eps REAL,

    dividend_payout REAL,


    FOREIGN KEY(company_id)
    REFERENCES companies(id)

);
CREATE TABLE IF NOT EXISTS balance_sheet (

    balance_id INTEGER PRIMARY KEY,

    id TEXT NOT NULL,

    year INTEGER,

    assets REAL,

    liabilities REAL,

    equity REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);


CREATE TABLE IF NOT EXISTS income_statement (

    income_id INTEGER PRIMARY KEY,

    id TEXT NOT NULL,

    revenue REAL,

    expense REAL,

    profit REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);
CREATE TABLE IF NOT EXISTS stock_prices (

    price_id INTEGER PRIMARY KEY,

    id TEXT,

    date TEXT,

    close_price REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);
CREATE TABLE IF NOT EXISTS dividends (

    dividend_id INTEGER PRIMARY KEY,

    id TEXT,

    dividend REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);

CREATE TABLE IF NOT EXISTS shareholding (

    holding_id INTEGER PRIMARY KEY,

    id TEXT,

    promoter REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);


CREATE TABLE IF NOT EXISTS ratios (

    ratio_id INTEGER PRIMARY KEY,

    id TEXT,

    pe_ratio REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);

CREATE TABLE IF NOT EXISTS market_cap (

    marketcap_id INTEGER PRIMARY KEY,

    id TEXT,

    market_cap REAL,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);

CREATE TABLE IF NOT EXISTS financial_period (

    period_id INTEGER PRIMARY KEY,

    id TEXT,

    period TEXT,

    FOREIGN KEY(id)
    REFERENCES companies(id)

);