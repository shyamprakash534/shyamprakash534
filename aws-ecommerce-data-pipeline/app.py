from pathlib import Path
import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="E-Commerce Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
BASE = Path(__file__).parent
OUT = BASE / "data" / "local_output"

@st.cache_data
def load_default_data():
    monthly = pd.read_csv(OUT / "monthly_sales.csv")
    cats = pd.read_csv(OUT / "top_categories.csv")
    late = pd.read_csv(OUT / "late_delivery_rate.csv")
    return monthly, cats, late

def process_upload(file):
    df = pd.read_csv(file)
    cols = {c.lower().strip().replace(" ", "_"): c for c in df.columns}
    if "order_year_month" in cols and "total_revenue" in cols:
        monthly = df.rename(columns={cols["order_year_month"]: "order_year_month", cols["total_revenue"]: "total_revenue"})
        if "num_orders" not in monthly: monthly["num_orders"] = 1
        if "avg_order_value" not in monthly: monthly["avg_order_value"] = monthly["total_revenue"] / monthly["num_orders"].replace(0, 1)
        cats = pd.DataFrame(columns=["product_category", "total_revenue", "num_orders"])
        late = pd.DataFrame(columns=["order_year_month", "delivered_orders", "late_pct"])
        return monthly, cats, late
    raise ValueError("CSV needs at least order_year_month and total_revenue columns.")

monthly, cats, late = load_default_data()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background:#f6f7fb}
.block-container {max-width:1450px;padding:1.8rem 2.5rem 3rem}
[data-testid="stSidebar"] {border-right:1px solid #e6e8ef}
.hero {background:linear-gradient(120deg,#111827,#243b64);padding:28px 32px;border-radius:20px;color:#fff;margin-bottom:20px}
.hero h1 {font-size:30px;margin:0;font-weight:750}.hero p {margin:7px 0 0;color:#d9e2f2;font-size:14px}
.card {background:#fff;border:1px solid #e6e8ef;border-radius:16px;padding:18px 20px;min-height:105px;box-shadow:0 2px 10px rgba(16,24,40,.04)}
.label {font-size:12px;color:#667085;font-weight:600}.value {font-size:25px;color:#101828;font-weight:750;margin-top:7px}.muted {font-size:12px;color:#98a2b3;margin-top:4px}
.section {font-size:20px;font-weight:700;color:#101828;margin:24px 0 12px}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>E-Commerce Analytics Dashboard</h1><p>Upload data, validate it, and turn it into decision-ready business insights.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Data Input")
    uploaded = st.file_uploader("Upload CSV", type=["csv"], help="CSV should contain order_year_month and total_revenue for the trend view.")
    if uploaded:
        try:
            monthly, uploaded_cats, uploaded_late = process_upload(io.BytesIO(uploaded.getvalue()))
            if not uploaded_cats.empty: cats = uploaded_cats
            if not uploaded_late.empty: late = uploaded_late
            st.success("Data loaded")
        except Exception as e:
            st.error(str(e))
    st.markdown("### Filters")
    metric = st.selectbox("Output metric", ["total_revenue", "num_orders", "avg_order_value"], format_func=lambda x: {"total_revenue":"Revenue", "num_orders":"Orders", "avg_order_value":"Average Order Value"}[x])
    show_unknown = st.checkbox("Include unknown category", value=False)
    st.caption("Default dataset is loaded automatically. Uploading a CSV replaces the monthly trend input.")

monthly["month"] = pd.to_datetime(monthly["order_year_month"])
revenue = pd.to_numeric(monthly["total_revenue"], errors="coerce").sum()
orders = pd.to_numeric(monthly["num_orders"], errors="coerce").sum()
aov = revenue / orders if orders else 0
late_rate = pd.to_numeric(late["late_pct"], errors="coerce").mean() if not late.empty else 0

cols = st.columns(4)
for col, label, value, sub in [
    (cols[0], "TOTAL REVENUE", f"${revenue:,.2f}", "From selected input"),
    (cols[1], "TOTAL ORDERS", f"{orders:,.0f}", "Validated order volume"),
    (cols[2], "AVG ORDER VALUE", f"${aov:,.2f}", "Revenue ÷ orders"),
    (cols[3], "LATE DELIVERY", f"{late_rate:.2f}%", "Average monthly rate"),
]:
    col.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="muted">{sub}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section">Analytics Output</div>', unsafe_allow_html=True)
t1, t2, t3 = st.tabs(["Trend", "Categories", "Delivery"])

with t1:
    title = {"total_revenue":"Revenue Trend", "num_orders":"Order Volume Trend", "avg_order_value":"Average Order Value Trend"}[metric]
    fig = px.line(monthly.sort_values("month"), x="month", y=metric, markers=True, title=title)
    fig.update_layout(height=410, margin=dict(l=10,r=10,t=55,b=10), hovermode="x unified", plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("View processed output"):
        st.dataframe(monthly.drop(columns=["month"], errors="ignore"), use_container_width=True, hide_index=True)
        st.download_button("Download output CSV", monthly.drop(columns=["month"], errors="ignore").to_csv(index=False), "monthly_output.csv", "text/csv")

with t2:
    cats_view = cats.copy()
    if not show_unknown and "product_category" in cats_view: cats_view = cats_view[cats_view["product_category"].str.lower() != "unknown"]
    if cats_view.empty:
        st.info("Category output is not available for the uploaded CSV.")
    else:
        fig = px.bar(cats_view.sort_values("total_revenue"), x="total_revenue", y="product_category", orientation="h", title="Revenue by Category", text_auto=".2s")
        fig.update_layout(height=450, margin=dict(l=10,r=10,t=55,b=10), plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(cats_view, use_container_width=True, hide_index=True)

with t3:
    if late.empty:
        st.info("Delivery output is not available for the uploaded CSV.")
    else:
        late["month"] = pd.to_datetime(late["order_year_month"])
        fig = px.line(late.sort_values("month"), x="month", y="late_pct", markers=True, title="Late Delivery Rate")
        fig.update_layout(height=410, margin=dict(l=10,r=10,t=55,b=10), yaxis_title="Late delivery %", plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(late.drop(columns=["month"], errors="ignore"), use_container_width=True, hide_index=True)

st.markdown('<div class="section">Pipeline</div>', unsafe_allow_html=True)
flow = st.columns(5)
for c, title, desc in zip(flow, ["Raw S3", "AWS Glue", "Curated S3", "Athena", "Dashboard"], ["Input data", "Transform + quality", "Analytics data", "SQL queries", "Business output"]):
    c.markdown(f'<div class="card"><b>{title}</b><br><span class="muted">{desc}</span></div>', unsafe_allow_html=True)

st.caption("Input → Processing → Output. The dashboard uses the validated repository dataset by default and supports CSV upload for interactive analysis.")
