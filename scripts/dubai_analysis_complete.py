"""
============================================================
DUBAI REAL ESTATE MARKET ANALYSIS - COMPLETE PROJECT
============================================================
Author     : [Your Name]
Dataset    : Dubai Land Department (DLD) Transactions 2023
             Source: Kaggle - Dubai Real Estate Transactions
Tools      : Python, Pandas, Matplotlib, Seaborn, SQLite
Business Q : Where should investors focus in Dubai? Which
             areas offer best value and market activity?
============================================================
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sqlite3
import os

# ============================================================
# SETUP
# ============================================================
os.makedirs("charts", exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "DejaVu Sans"

BLUE = "#1F4E78"; ORANGE = "#F18F01"; GREEN = "#048A81"
RED = "#C0392B"; PURPLE = "#8E44AD"

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_excel("cleaned_dubai_real_estate.xlsx")
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
df["Month"] = df["Transaction Date"].dt.strftime("%Y-%m")
df["Year"] = df["Transaction Date"].dt.year

print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")

# Key subsets
sales_unit = df[(df["Transaction Type"]=="Sales") & (df["Property Type"]=="Unit")]
flats = sales_unit[sales_unit["Property Sub Type"]=="Flat"]
freehold = sales_unit[sales_unit["Is Free Hold?"]=="Free Hold"]

# ============================================================
# 2. PYTHON ANALYSIS - EXPLORATORY
# ============================================================

# -- KPI Summary --
print("\n=== KEY METRICS ===")
print(f"Total Transactions       : {len(df):,}")
print(f"Total Sales Value        : AED {df[df['Transaction Type']=='Sales']['Amount'].sum()/1e9:.1f} Billion")
print(f"Avg Residential Price    : AED {sales_unit['Prize per sq meter'].mean():,.0f} / sq.m")
print(f"Median Residential Price : AED {sales_unit['Prize per sq meter'].median():,.0f} / sq.m")
print(f"Total Unique Areas       : {df['Area'].nunique()}")
print(f"Freehold Transactions    : {len(freehold):,} ({len(freehold)/len(sales_unit)*100:.0f}% of sales)")

# -- Top 10 Expensive Areas (min 30 txns) --
top_areas = (sales_unit.groupby("Area")["Prize per sq meter"]
             .agg(["mean","count"])
             .query("count >= 30")
             .sort_values("mean", ascending=False)
             .head(10))

fig, ax = plt.subplots(figsize=(9,5))
sns.barplot(x=top_areas["mean"], y=top_areas.index, hue=top_areas.index,
            palette="Blues_r", legend=False, ax=ax)
ax.set_xlabel("Avg Price per sq.m (AED)")
ax.set_title("Top 10 Most Expensive Areas", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("charts/01_top_areas.png", dpi=150); plt.close()

# -- Monthly Volume + Price Dual Axis --
m_vol = df.groupby("Month").size()
m_price = sales_unit.groupby("Month")["Prize per sq meter"].mean()
fig, ax1 = plt.subplots(figsize=(10,5))
ax2 = ax1.twinx()
ax1.bar(m_vol.index, m_vol.values, color=BLUE, alpha=0.4, label="Transactions")
ax2.plot(m_price.index, m_price.values, color=ORANGE, marker="o", lw=2.5, label="Avg Price/sqm")
ax1.set_ylabel("Number of Transactions", color=BLUE)
ax2.set_ylabel("Avg Price per sq.m (AED)", color=ORANGE)
ax1.set_title("Monthly Volume vs Avg Price Trend", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("charts/02_monthly_trend.png", dpi=150); plt.close()

# -- Price Distribution (capped at 95th pct) --
cap = sales_unit["Amount"].quantile(0.95)
fig, ax = plt.subplots(figsize=(9,5))
sns.histplot(sales_unit[sales_unit["Amount"]<=cap]["Amount"], bins=40, color=BLUE, ax=ax)
ax.set_xlabel("Transaction Amount (AED)")
ax.set_title("Price Distribution - Residential Sales (95th pct cap)", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("charts/03_price_dist.png", dpi=150); plt.close()

# -- Correlation Heatmap --
num_cols = flats[["Amount","Property Size (sq.m)","Prize per sq meter","No. of Buyer","No. of Seller"]]
fig, ax = plt.subplots(figsize=(7,5))
mask = np.triu(np.ones(num_cols.corr().shape, dtype=bool))
sns.heatmap(num_cols.corr(), annot=True, fmt=".2f", cmap="coolwarm",
            mask=mask, square=True, linewidths=0.5, ax=ax)
ax.set_title("Correlation Matrix (Flat Sales)", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("charts/04_correlation.png", dpi=150); plt.close()

# -- Freehold vs Non-Freehold --
fh_price = sales_unit.groupby("Is Free Hold?")["Prize per sq meter"].mean()
fig, ax = plt.subplots(figsize=(6,5))
fh_price.plot(kind="bar", color=[ORANGE, GREEN], ax=ax, width=0.5)
ax.set_title("Freehold vs Non-Freehold: Avg Price/sq.m", fontsize=13, fontweight="bold")
ax.set_ylabel("AED"); ax.tick_params(axis="x", rotation=0)
plt.tight_layout(); plt.savefig("charts/05_freehold.png", dpi=150); plt.close()

print("\nAll charts saved to /charts folder")

# ============================================================
# 3. SQL ANALYSIS (SQLite)
# ============================================================
conn = sqlite3.connect("dubai_real_estate.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

sql_queries = {
    "Area Summary": """
        SELECT Area, COUNT(*) AS transactions,
            ROUND(AVG(Amount),0) AS avg_price,
            ROUND(AVG([Prize per sq meter]),0) AS avg_sqm,
            ROUND(SUM(Amount)/1000000,1) AS total_value_m
        FROM transactions
        WHERE [Transaction Type]="Sales" AND [Property Type]="Unit"
        GROUP BY Area HAVING COUNT(*) >= 30
        ORDER BY avg_sqm DESC LIMIT 15
    """,
    "Monthly KPI": """
        SELECT strftime('%Y-%m',[Transaction Date]) AS month,
            COUNT(*) AS transactions,
            ROUND(AVG([Prize per sq meter]),0) AS avg_sqm,
            ROUND(SUM(Amount)/1000000,1) AS total_value_m
        FROM transactions GROUP BY month ORDER BY month
    """,
    "Freehold Effect": """
        SELECT [Is Free Hold?], COUNT(*) AS count,
            ROUND(AVG([Prize per sq meter]),0) AS avg_sqm
        FROM transactions WHERE [Transaction Type]="Sales" AND [Property Type]="Unit"
        GROUP BY [Is Free Hold?]
    """,
    "Top Projects": """
        SELECT Project, COUNT(*) AS txns,
            ROUND(AVG([Prize per sq meter]),0) AS avg_sqm
        FROM transactions
        WHERE [Transaction Type]="Sales" AND Project!="Not Available"
        GROUP BY Project HAVING txns >= 20
        ORDER BY avg_sqm DESC LIMIT 10
    """
}

print("\n=== SQL RESULTS ===")
for name, q in sql_queries.items():
    result = pd.read_sql_query(q, conn)
    print(f"\n[{name}]")
    print(result.to_string(index=False))

conn.close()
print("\nProject Complete! Charts saved. SQL analysis done.")
