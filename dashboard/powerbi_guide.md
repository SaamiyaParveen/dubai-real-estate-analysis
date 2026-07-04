# Power BI Dashboard Guide - Dubai Real Estate Analysis

## Step 1: Data Import
1. Open Power BI Desktop (free download from Microsoft)
2. Click "Get Data" → Excel → select `powerbi_ready_data.xlsx`
3. Import all 4 sheets:
   - `fact_transactions` (main data - 79,667 rows)
   - `dim_area_summary` (area level summary)
   - `agg_monthly_kpi` (month wise KPIs)
   - `top_areas_geo` (top 20 areas for map)

## Step 2: Relationships (Model View)
- fact_transactions[area] → dim_area_summary[Area]
- fact_transactions[year_month] → agg_monthly_kpi[year_month]

## Step 3: Create These DAX Measures
```
Total Transactions = COUNTROWS(fact_transactions)
Total Sales Value (AED Bn) = DIVIDE(SUMX(FILTER(fact_transactions, fact_transactions[transaction_type]="Sales"), fact_transactions[amount_aed]), 1000000000)
Avg Price per sqm = AVERAGE(fact_transactions[price_per_sqm])
Median Price per sqm = MEDIAN(fact_transactions[price_per_sqm])
Freehold % = DIVIDE(COUNTROWS(FILTER(fact_transactions, fact_transactions[is_freehold]="Free Hold")), COUNTROWS(fact_transactions))
```

## Step 4: Build These Visuals

### Page 1 - Executive Summary (KPI Cards)
- Card: Total Transactions (79,667)
- Card: Total Sales Value in AED Billion (176.5 Bn)
- Card: Avg Price/sqm (18,464 AED)
- Card: Freehold % (94.7%)
- Donut: Property Type Distribution
- Bar: Transaction Type Breakdown

### Page 2 - Area Analysis
- Bar Chart: Top 10 Areas by Avg Price/sqm (from dim_area_summary)
- Map Visual: Area → total_value_million (bubble size on UAE map)
  * Use "Area" column as location, "total_value_m" as bubble size
- Table: Top 15 areas with transactions, avg_price, total_value

### Page 3 - Trends & Time
- Line Chart: year_month → total_transactions (from agg_monthly_kpi)
- Line Chart: year_month → avg_price_sqm (from agg_monthly_kpi)
- Combo Chart (dual axis): volume bars + price line together

### Page 4 - Investment Insights
- Clustered Bar: Freehold vs Non-Freehold (avg price, count)
- Bar: Top Projects by price/sqm
- Bar: Nearest Mall vs avg price
- Scatter: transactions vs avg_price_sqm (from top_areas_geo)

## Step 5: Slicers (Filters) to Add
- Transaction Type (Sales / Mortgage / Gifts)
- Property Type (Unit / Land / Building)
- Is Freehold (Free Hold / Non Free Hold)
- Year Month (date slicer)
- Area (search/dropdown)

## Step 6: Formatting Tips
- Theme: Use "Executive" or custom colors (#1F4E78 blue, #F18F01 orange)
- Font: Segoe UI throughout
- Add Dubai skyline image as background (optional)
- Turn on Data Labels on all charts
- Add tooltips: hover pe area name + price + transactions dikhe

## Step 7: Key Insights to Highlight (Pre-built text boxes in Power BI)
1. "Bluewaters & Zaabeel First are Dubai's most premium areas at 48K+ AED/sqm"
2. "March 2023 saw peak activity with 16,400+ transactions"
3. "Freehold properties command 2.5x premium over Non-Freehold"
4. "JVC leads in volume - best for mid-market investors"
5. "Dubai Mall proximity correlates with 21,845 AED/sqm avg price"
