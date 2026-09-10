from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AWS E-Commerce Data Pipeline", page_icon="☁️", layout="wide")
BASE = Path(__file__).parent
OUT = BASE / "data" / "local_output"

@st.cache_data
def load_data():
    monthly = pd.read_csv(OUT / "monthly_sales.csv")
    cats = pd.read_csv(OUT / "top_categories.csv")
    late = pd.read_csv(OUT / "late_delivery_rate.csv")
    return monthly, cats, late

monthly, cats, late = load_data()
monthly["month"] = pd.to_datetime(monthly["order_year_month"])
late["month"] = pd.to_datetime(late["order_year_month"])

st.markdown("""
<style>
.main {background:#f7f9fc}
.block-container {max-width:1400px;padding-top:2rem}
.hero {padding:1.4rem 1.6rem;border-radius:18px;background:linear-gradient(135deg,#101828,#1d4ed8);color:white;margin-bottom:1rem}
.hero h1 {margin:0;font-size:2.2rem}.hero p {margin:.45rem 0 0;color:#dbeafe}
.card {background:white;border:1px solid #e5e7eb;border-radius:16px;padding:1rem 1.1rem;box-shadow:0 4px 18px rgba(15,23,42,.05)}
.label {font-size:.78rem;color:#667085}.value {font-size:1.65rem;font-weight:750;color:#101828}.muted {color:#667085;font-size:.86rem}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>AWS E-Commerce Data Pipeline</h1><p>Local validation outputs presented as a production-style analytics layer for the AWS Glue → S3 → Athena architecture.</p></div>', unsafe_allow_html=True)

revenue = monthly["total_revenue"].sum()
orders = int(monthly["num_orders"].sum())
aov = revenue / orders if orders else 0
late_rate = late["late_pct"].mean()

cols = st.columns(4)
for col, label, value, sub in [
    (cols[0], "Total Revenue", f"${revenue:,.2f}", "Curated delivered-order revenue"),
    (cols[1], "Delivered Orders", f"{orders:,}", "Validated analytical orders"),
    (cols[2], "Average Order Value", f"${aov:,.2f}", "Revenue ÷ delivered orders"),
    (cols[3], "Avg Late Delivery", f"{late_rate:.2f}%", "Across monthly delivery cohorts"),
]:
    col.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="muted">{sub}</div></div>', unsafe_allow_html=True)

st.sidebar.header("Pipeline Controls")
metric = st.sidebar.selectbox("Trend metric", ["total_revenue", "num_orders", "avg_order_value"])
show_unknown = st.sidebar.checkbox("Show unknown category", value=False)

cats_view = cats if show_unknown else cats[cats["product_category"] != "unknown"].copy()

st.subheader("Analytics Output")
t1, t2, t3 = st.tabs(["Revenue Trend", "Top Categories", "Delivery Quality"])

with t1:
    title = {"total_revenue":"Monthly Revenue", "num_orders":"Monthly Delivered Orders", "avg_order_value":"Monthly Average Order Value"}[metric]
    fig = px.line(monthly, x="month", y=metric, markers=True, title=title)
    fig.update_layout(height=430, margin=dict(l=10,r=10,t=55,b=10), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(monthly.drop(columns=["month"]), use_container_width=True, hide_index=True)

with t2:
    fig = px.bar(cats_view.sort_values("total_revenue"), x="total_revenue", y="product_category", orientation="h", title="Revenue by Product Category", text_auto=".2s")
    fig.update_layout(height=480, margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(cats_view, use_container_width=True, hide_index=True)

with t3:
    fig = px.line(late, x="month", y="late_pct", markers=True, title="Monthly Late Delivery Rate")
    fig.update_layout(height=430, margin=dict(l=10,r=10,t=55,b=10), yaxis_title="Late delivery %")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(late.drop(columns=["month"]), use_container_width=True, hide_index=True)

st.divider()
st.subheader("Pipeline Architecture")
flow = st.columns(5)
for c, title, desc in zip(flow, ["Raw S3", "AWS Glue", "Curated S3", "Athena", "BI / Dashboard"], ["CSV landing zone", "DQ + PySpark ETL", "Parquet analytical zone", "Serverless SQL", "Decision-ready metrics"]):
    c.markdown(f'<div class="card"><b>{title}</b><br><span class="muted">{desc}</span></div>', unsafe_allow_html=True)

st.caption("Demo analytics use the repository's local validation outputs. AWS resources are provisioned separately with Terraform; no AWS credentials are required by this dashboard.")
