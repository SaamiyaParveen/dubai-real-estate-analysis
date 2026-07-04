-- ============================================================
-- Dubai Real Estate Market Analysis - SQL Queries
-- Database: SQLite | Tool: Python sqlite3 / DB Browser
-- Dataset: DLD Transactions Jan-Jun 2023 | 79,667 Records
-- Author: Saamiya Parveen
-- ============================================================

-- Q1: Top 15 Most Expensive Areas (Residential Units)
SELECT 
    Area,
    COUNT(*) AS total_transactions,
    ROUND(AVG(Amount), 0) AS avg_price_aed,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_per_sqm,
    ROUND(SUM(Amount)/1000000, 1) AS total_value_million_aed
FROM transactions
WHERE "Transaction Type" = 'Sales' 
  AND "Property Type" = 'Unit'
GROUP BY Area
HAVING COUNT(*) >= 30
ORDER BY avg_price_per_sqm DESC
LIMIT 15;

-- Q2: Monthly Transaction Volume & Avg Price Trend
SELECT 
    strftime('%Y-%m', "Transaction Date") AS month,
    COUNT(*) AS total_transactions,
    ROUND(SUM(Amount)/1000000, 1) AS total_value_million_aed,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_per_sqm
FROM transactions
GROUP BY month
ORDER BY month;

-- Q3: Freehold vs Non-Freehold Price Comparison
SELECT 
    "Is Free Hold?" AS ownership_type,
    COUNT(*) AS total_transactions,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_sqm,
    ROUND(AVG(Amount), 0) AS avg_total_price
FROM transactions
WHERE "Transaction Type" = 'Sales' 
  AND "Property Type" = 'Unit'
GROUP BY "Is Free Hold?";

-- Q4: Top 10 Premium Projects by Price/sqm
SELECT 
    Project,
    COUNT(*) AS transactions,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_sqm,
    ROUND(AVG(Amount), 0) AS avg_total_price
FROM transactions
WHERE "Transaction Type" = 'Sales' 
  AND Project != 'Not Available'
GROUP BY Project
HAVING COUNT(*) >= 20
ORDER BY avg_price_sqm DESC
LIMIT 10;

-- Q5: Best Investment Zones (Freehold, High Volume)
SELECT 
    Area,
    COUNT(*) AS transactions,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_sqm,
    ROUND(AVG(Amount), 0) AS avg_deal_value
FROM transactions
WHERE "Transaction Type" = 'Sales'
  AND "Property Type" = 'Unit'
  AND "Is Free Hold?" = 'Free Hold'
GROUP BY Area
HAVING COUNT(*) >= 50
ORDER BY transactions DESC
LIMIT 12;

-- Q6: Mall Proximity Effect on Price
SELECT 
    "Nearest Mall",
    COUNT(*) AS transactions,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_sqm
FROM transactions
WHERE "Transaction Type" = 'Sales'
  AND "Property Type" = 'Unit'
  AND "Nearest Mall" != 'Not Available'
GROUP BY "Nearest Mall"
HAVING COUNT(*) >= 50
ORDER BY avg_price_sqm DESC;

-- Q7: Property Sub-Type Analysis
SELECT
    "Property Sub Type",
    COUNT(*) AS transactions,
    ROUND(AVG("Prize per sq meter"), 0) AS avg_price_sqm
FROM transactions
WHERE "Transaction Type" = 'Sales'
  AND "Property Type" = 'Unit'
GROUP BY "Property Sub Type"
ORDER BY transactions DESC;

-- Q8: Month-wise Sales vs Mortgage vs Gifts
SELECT 
    strftime('%Y-%m', "Transaction Date") AS month,
    SUM(CASE WHEN "Transaction Type"='Sales' THEN 1 ELSE 0 END) AS sales_count,
    SUM(CASE WHEN "Transaction Type"='Mortgage' THEN 1 ELSE 0 END) AS mortgage_count,
    SUM(CASE WHEN "Transaction Type"='Gifts' THEN 1 ELSE 0 END) AS gifts_count
FROM transactions
GROUP BY month
ORDER BY month;
