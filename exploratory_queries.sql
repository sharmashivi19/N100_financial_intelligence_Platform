-- Total companies

SELECT COUNT(*) AS total_companies
FROM companies;


-- Company list

SELECT
    id,
    company_name
FROM companies
LIMIT 10;


-- Financial records

SELECT COUNT(*) AS total_financial_records
FROM financials;


-- Highest sales companies

SELECT
    company_id,
    MAX(sales) AS highest_sales
FROM financials
GROUP BY company_id
ORDER BY highest_sales DESC
LIMIT 10;


-- Average ROE

SELECT
    AVG(roe_percentage) AS avg_roe
FROM companies;


-- Year coverage

SELECT
    MIN(year) AS first_year,
    MAX(year) AS last_year
FROM financials;


-- Stock price count

SELECT COUNT(*) AS price_records
FROM stock_prices;


-- Top companies by ROCE

SELECT
    id,
    company_name,
    roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;