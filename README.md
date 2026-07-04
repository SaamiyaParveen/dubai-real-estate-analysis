# 🏙️ Dubai Real Estate Market Analysis — H1 2023

> End-to-end data analysis of 79,667 DLD transactions  
> to identify high-value investment zones and market trends in Dubai.

---

## 📌 Business Problem

**"Which areas in Dubai offer the best real estate investment opportunity based on price, volume, and ownership type?"**

This project analyzes official Dubai Land Department (DLD) transaction data from January to June 2023 to answer this question using data-driven insights.

---

## 🔑 Key Findings

- 🏆 **Bluewaters Island** is Dubai's most expensive residential area at **48,639 AED/sqm** — not Palm Jumeirah (ranked 6th)
- 📊 **JVC leads in market activity** with 6,378 transactions at an accessible 11,732 AED/sqm — best for mid-market investors
- 💰 **Freehold properties command 150% premium** over Non-Freehold (18,707 vs 7,471 AED/sqm)
- 📈 **Average price rose from 15,142 → 16,087 AED/sqm** (Jan → Jun 2023) — clear upward trajectory
- 🏢 **73.8% of transactions are residential units** — apartment-driven market
- 💵 **Total market value: AED 176.5 Billion** in just 6 months

---

## 🛠️ Tools & Technologies

| Tool | Usage |
|------|-------|
| **Excel** | Initial data exploration, outlier detection |
| **Python (Pandas, Matplotlib, Seaborn)** | Data cleaning, EDA, 20+ visualizations |
| **SQL (SQLite)** | 8 analytical queries, aggregations |
| **Interactive Dashboard (HTML/JS)** | 4-page interactive dashboard | 

---

## 📊 Dashboard

Open `dashboard/Dubai_Real_Estate_Dashboard.html` directly in any browser — no software needed.

**4 Pages:**
- Executive Overview — KPIs + market structure
- Area Analysis — price vs volume by neighbourhood  
- Market Trends — monthly patterns
- Investment Insights — freehold zones + project ranking

---

## 🔄 Data Cleaning Summary

| Step | Action | Impact |
|------|--------|--------|
| Duplicate removal | Removed identical rows | 1,874 deleted |
| Outlier removal | Removed Unit category errors | 8 deleted |
| Missing values | Filled with Not Available | ~27,000 cells |
| Feature engineering | Added Price per sq.m column | 79,667 rows |
| **Final dataset** | **Clean, analysis-ready** | **79,667 rows** |

---

## 📂 Dataset Source

- **Source:** Kaggle — Dubai Real Estate Transactions Dataset
- **Original:** Dubai Land Department (DLD) official records
- **Period:** January 2023 – June 2023
- **Records:** 79,667 transactions across 258 areas

---

*Built as part of Data Analyst portfolio — targeting UAE/Dubai opportunities*

---
