# E-Commerce Sales, Customer & Profitability Analytics Platform

Portfolio-grade analytics dashboard inspired by the supplied Power BI executive dashboard design.

## Live application
Deployed on Render as a Streamlit web service.

## Features
- Five analytical pages: Executive Overview, Sales & Profitability, Customer Analytics, Product & Category, Regional Performance.
- Interactive Region, Category, Segment and date filters.
- Revenue, profit, margin, discount and margin-leakage KPIs.
- Monthly MoM revenue growth and cumulative revenue/profit trajectory.
- Customer segmentation, Pareto deciles and buyer-frequency analysis.
- Product/sub-category profitability diagnostics.
- Regional financial and logistics analysis.
- Deterministic synthetic e-commerce data generated with NumPy seed 42 when the app starts from a clean checkout.

## Stack
Python, Pandas, NumPy, Plotly, Streamlit

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

The original project package also contains the fuller Power BI/DAX/SQL/data-validation assets supplied for this portfolio project.