import streamlit as st
import pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="E-Commerce Analytics", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

BASE = Path(__file__).parent
DATA = BASE / "data"
CLEAN = DATA / "cleaned"

# -----------------------------
# Data generation / loading
# -----------------------------
def build_data():
    rng = np.random.default_rng(42)
    CLEAN.mkdir(parents=True, exist_ok=True)
    geo = pd.DataFrame([
        ["10001","New York","New York","East"],["19104","Philadelphia","Pennsylvania","East"],["02138","Boston","Massachusetts","East"],
        ["90001","Los Angeles","California","West"],["94102","San Francisco","California","West"],["98101","Seattle","Washington","West"],
        ["60601","Chicago","Illinois","Central"],["48201","Detroit","Michigan","Central"],["75201","Dallas","Texas","Central"],
        ["77001","Houston","Texas","Central"],["30301","Atlanta","Georgia","South"],["33101","Miami","Florida","South"],
        ["27601","Raleigh","North Carolina","South"],["80202","Denver","Colorado","West"],["85001","Phoenix","Arizona","West"]
    ], columns=["postal_code","city","state","region"])
    cats = pd.DataFrame([
        ["Technology","Phones",.22],["Technology","Accessories",.35],["Technology","Copiers",.40],["Technology","Machines",.05],
        ["Furniture","Chairs",.18],["Furniture","Tables",-.08],["Furniture","Bookcases",.12],["Furniture","Furnishings",.25],
        ["Office Supplies","Storage",.20],["Office Supplies","Binders",.32],["Office Supplies","Paper",.42],["Office Supplies","Art",.30],["Office Supplies","Appliances",.28],["Office Supplies","Envelopes",.38]
    ], columns=["category","sub_category","target_margin"])
    products=[]; pid=1001
    for _, c in cats.iterrows():
        for j in range(4):
            price=float(rng.uniform(450,1800) if c.sub_category in ["Copiers","Machines","Tables"] else rng.uniform(30,600))
            if c.sub_category in ["Binders","Paper","Art","Envelopes"]: price=float(rng.uniform(8,45))
            cost=price*(1-float(c.target_margin+rng.uniform(-.05,.05)))
            products.append([f"PRD-{pid}",f"{c.sub_category} Product {j+1}",c.category,c.sub_category,round(price,2),round(max(cost,price*.4),2)])
            pid+=1
    products=pd.DataFrame(products,columns=["product_id","product_name","category","sub_category","base_price","cost_price"])
    segs=rng.choice(["Consumer","Corporate","Home Office"],1250,p=[.52,.30,.18]); geo_pick=rng.integers(0,len(geo),1250)
    customers=pd.DataFrame({"customer_id":[f"CUST-{i:04d}" for i in range(1,1251)],"customer_segment":segs,"postal_code":geo.iloc[geo_pick].postal_code.values})
    orders=[]; items=[]; oid=10001; iid=50001
    for _,cu in customers.iterrows():
        n=int(rng.choice([1,2,3,4,5,6,7],p=[.45,.14,.14,.10,.07,.06,.04]))
        for _ in range(n):
            d=pd.Timestamp("2022-01-01")+pd.Timedelta(days=int(rng.integers(0,730)))
            mode=rng.choice(["Standard Class","Second Class","First Class","Same Day"],p=[.59,.20,.15,.06])
            delay={"Standard Class":5,"Second Class":3,"First Class":2,"Same Day":0}[mode]+int(rng.integers(0,2))
            status=rng.choice(["Delivered","Shipped","Cancelled","Returned"],p=[.89,.04,.04,.03])
            order=f"ORD-{oid}"; oid+=1
            orders.append([order,cu.customer_id,d,d+pd.Timedelta(days=delay),mode,status,cu.postal_code,cu.customer_segment])
            picks=products.iloc[rng.choice(len(products),size=int(rng.choice([1,2,3],p=[.5,.35,.15])),replace=False)]
            for pr in picks.itertuples():
                q=int(rng.choice([1,2,3,4,5],p=[.55,.25,.12,.05,.03]))
                if pr.sub_category=="Tables": disc=float(rng.choice([.15,.25,.35,.45,.55],p=[.1,.25,.3,.25,.1]))
                elif pr.sub_category=="Machines": disc=float(rng.choice([.1,.2,.3,.4],p=[.2,.4,.3,.1]))
                else: disc=float(rng.choice([0,.05,.1,.15,.2],p=[.45,.25,.15,.1,.05]))
                gross=q*pr.base_price; net=gross*(1-disc); cost=q*pr.cost_price
                items.append([f"ITEM-{iid}",order,pr.product_id,q,pr.base_price,disc,net,cost,net-cost]); iid+=1
    orders=pd.DataFrame(orders,columns=["order_id","customer_id","order_date","ship_date","ship_mode","order_status","postal_code","customer_segment"])
    items=pd.DataFrame(items,columns=["order_item_id","order_id","product_id","quantity","unit_price","discount_pct","line_total","line_cost","line_profit"])
    for df,name in [(geo,"geography"),(cats,"categories"),(products,"products"),(customers,"customers"),(orders,"orders"),(items,"order_items")]:
        df.to_csv(CLEAN/f"{name}.csv",index=False)

def load_data():
    if not (CLEAN/"orders.csv").exists(): build_data()
    g=pd.read_csv(CLEAN/"geography.csv")
    p=pd.read_csv(CLEAN/"products.csv")
    o=pd.read_csv(CLEAN/"orders.csv",parse_dates=["order_date","ship_date"])
    i=pd.read_csv(CLEAN/"order_items.csv")
    f=i.merge(o,on="order_id").merge(p,on="product_id").merge(g,on="postal_code")
    f["gross_line"]=f.quantity*f.unit_price
    f["discount_amount"]=f.gross_line-f.line_total
    f["delivery_days"]=(f.ship_date-f.order_date).dt.days
    f["month"]=f.order_date.dt.to_period("M").dt.to_timestamp()
    return f

F=load_data()
F=F[F.order_status.isin(["Delivered","Shipped"])].copy()

# -----------------------------
# UI helpers
# -----------------------------
def money(x):
    if abs(x)>=1e6: return f"${x/1e6:.2f}M"
    if abs(x)>=1e3: return f"${x/1e3:.1f}K"
    return f"${x:,.0f}"

def pct(x): return f"{x*100:.2f}%"

def chart(fig, height=340):
    fig.update_layout(
        template="plotly_dark", height=height,
        margin=dict(l=8,r=8,t=48,b=12),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(color="#E5E7EB", size=12),
        title_font=dict(size=16, color="#F9FAFB"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

# -----------------------------
# Clean visual system
# -----------------------------
st.markdown("""
<style>
:root { --bg:#0B1120; --panel:#111827; --panel2:#172033; --border:#26344A; --muted:#94A3B8; --text:#F8FAFC; --accent:#60A5FA; }
.stApp { background:var(--bg); color:var(--text); }
.block-container { max-width:1500px; padding-top:2rem; padding-bottom:3rem; }
[data-testid="stSidebar"] { background:#0F172A; border-right:1px solid var(--border); }
[data-testid="stSidebar"] .block-container { padding-top:1.4rem; }
[data-testid="stMetric"] { background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:14px 16px; }
[data-testid="stMetricLabel"] { color:var(--muted) !important; font-size:12px !important; }
[data-testid="stMetricValue"] { color:var(--text) !important; font-size:27px !important; }
.kicker { color:#93C5FD; font-size:12px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; margin-bottom:6px; }
.hero { background:linear-gradient(135deg,#111827,#172033); border:1px solid var(--border); border-radius:18px; padding:22px 24px; margin-bottom:18px; }
.hero h1 { margin:0; font-size:31px; letter-spacing:-.02em; }
.hero p { margin:7px 0 0; color:var(--muted); font-size:14px; }
.section { color:#CBD5E1; font-size:15px; font-weight:700; margin:18px 0 10px; }
.insight { background:#0F172A; border:1px solid var(--border); border-radius:12px; padding:12px 14px; color:#CBD5E1; font-size:13px; }
.small { color:var(--muted); font-size:12px; }
div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:12px; overflow:hidden; }
button[kind="secondary"] { border-color:var(--border); }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# INPUTS: sidebar
# -----------------------------
st.sidebar.markdown("## E-Commerce Analytics")
st.sidebar.caption("Clean inputs → clear business outputs")
st.sidebar.divider()
st.sidebar.markdown("### INPUTS")

page = st.sidebar.radio("Analysis view", [
    "Executive Overview", "Sales & Profitability", "Customer Analytics", "Product & Category", "Regional Performance"
], index=0)
region = st.sidebar.selectbox("Region", ["All"] + sorted(F.region.unique()))
category = st.sidebar.selectbox("Category", ["All"] + sorted(F.category.unique()))
segment = st.sidebar.selectbox("Customer Segment", ["All"] + sorted(F.customer_segment.unique()))
start = st.sidebar.date_input("Start date", F.order_date.min().date())
end = st.sidebar.date_input("End date", F.order_date.max().date())

if start > end:
    st.error("Start date must be before or equal to end date.")
    st.stop()

X = F[(F.order_date.dt.date >= start) & (F.order_date.dt.date <= end)].copy()
if region != "All": X = X[X.region == region]
if category != "All": X = X[X.category == category]
if segment != "All": X = X[X.customer_segment == segment]

# -----------------------------
# OUTPUTS: KPI layer
# -----------------------------
net = X.line_total.sum(); profit = X.line_profit.sum(); gross = X.gross_line.sum()
orders = X.order_id.nunique(); customers = X.customer_id.nunique(); units = X.quantity.sum()
margin = profit/net if net else 0; disc = (gross-net)/gross if gross else 0
leak = -X.loc[X.discount_pct > .20, "line_profit"].sum()
aov = net/orders if orders else 0

st.markdown(f"""
<div class="hero">
  <div class="kicker">OUTPUTS · {page}</div>
  <h1>E-Commerce Business Intelligence Dashboard</h1>
  <p>Interactive performance analysis for {start.strftime('%d %b %Y')} → {end.strftime('%d %b %Y')}. Use the INPUTS panel to change the result set.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">Key outputs</div>', unsafe_allow_html=True)
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Net Revenue", money(net), f"Gross {money(gross)}")
k2.metric("Net Profit", money(profit), f"Margin {pct(margin)}")
k3.metric("Orders", f"{orders:,}", f"AOV {money(aov)}")
k4.metric("Customers", f"{customers:,}", f"Units {units:,}")
k5.metric("Discount Rate", pct(disc), f"Leakage {money(leak)}")

# -----------------------------
# PAGES
# -----------------------------
if page == "Executive Overview":
    st.markdown('<div class="section">Business performance</div>', unsafe_allow_html=True)
    m=X.groupby("month",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"))
    fig=go.Figure([
        go.Scatter(x=m.month,y=m.revenue,name="Revenue",mode="lines+markers"),
        go.Scatter(x=m.month,y=m.profit,name="Profit",mode="lines+markers",yaxis="y2")
    ])
    fig.update_layout(title="Monthly Revenue & Profit", yaxis=dict(title="Revenue"), yaxis2=dict(title="Profit",overlaying="y",side="right"))
    st.plotly_chart(chart(fig,410), use_container_width=True)
    a,b=st.columns(2)
    seg=X.groupby("customer_segment",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"))
    a.plotly_chart(chart(px.bar(seg,x="customer_segment",y=["revenue","profit"],barmode="group",title="Revenue vs Profit by Segment")),use_container_width=True)
    reg=X.groupby("region",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"))
    b.plotly_chart(chart(px.bar(reg,x="region",y="revenue",title="Revenue by Region")),use_container_width=True)

elif page == "Sales & Profitability":
    st.markdown('<div class="section">Profitability outputs</div>', unsafe_allow_html=True)
    m=X.groupby("month",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"))
    m["mom"]=m.revenue.pct_change()*100; m["cum_rev"]=m.revenue.cumsum(); m["cum_profit"]=m.profit.cumsum()
    a,b=st.columns(2)
    a.plotly_chart(chart(px.bar(m,x="month",y="mom",title="Month-over-Month Revenue Growth (%)")),use_container_width=True)
    fig=go.Figure([go.Scatter(x=m.month,y=m.cum_rev,name="Cumulative Revenue"),go.Scatter(x=m.month,y=m.cum_profit,name="Cumulative Profit",yaxis="y2")])
    fig.update_layout(title="Cumulative Revenue & Profit",yaxis2=dict(overlaying="y",side="right"))
    b.plotly_chart(chart(fig),use_container_width=True)
    s=X.groupby("sub_category",as_index=False).agg(gross=("gross_line","sum"),revenue=("line_total","sum"),profit=("line_profit","sum"))
    s["discount"]=1-s.revenue/s.gross; s["margin"]=s.profit/s.revenue
    st.plotly_chart(chart(px.scatter(s,x="discount",y="margin",size="gross",hover_name="sub_category",title="Discount Rate vs Profit Margin")),use_container_width=True)

elif page == "Customer Analytics":
    st.markdown('<div class="section">Customer outputs</div>', unsafe_allow_html=True)
    s=X.groupby("customer_segment",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"),customers=("customer_id","nunique"))
    s["margin"]=s.profit/s.revenue
    a,b=st.columns(2)
    a.plotly_chart(chart(px.bar(s,x="customer_segment",y=["revenue","profit"],barmode="group",title="Segment Revenue vs Profit")),use_container_width=True)
    cu=X.groupby("customer_id").agg(revenue=("line_total","sum"),orders=("order_id","nunique")).sort_values("revenue",ascending=False).reset_index()
    if len(cu) >= 10:
        cu["decile"]=pd.qcut(np.arange(1,len(cu)+1),10,labels=[f"D{i}" for i in range(1,11)])
        d=cu.groupby("decile",observed=False).revenue.sum().reset_index(); d["share"]=100*d.revenue/d.revenue.sum()
        b.plotly_chart(chart(px.bar(d,x="decile",y="share",title="Spend Distribution by Customer Decile")),use_container_width=True)
    freq=X.groupby("customer_id").order_id.nunique().value_counts().sort_index().reset_index(); freq.columns=["orders","customers"]
    st.plotly_chart(chart(px.bar(freq,x="orders",y="customers",title="Buyer Frequency Distribution")),use_container_width=True)

elif page == "Product & Category":
    st.markdown('<div class="section">Product outputs</div>', unsafe_allow_html=True)
    s=X.groupby(["category","sub_category"],as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"),gross=("gross_line","sum"))
    s["margin"]=s.profit/s.revenue; s["discount"]=1-s.revenue/s.gross
    a,b=st.columns(2)
    a.plotly_chart(chart(px.bar(s.sort_values("profit"),x="profit",y="sub_category",orientation="h",title="Sub-Category Profit / Loss")),use_container_width=True)
    p=X.groupby("product_name",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum")).nlargest(10,"revenue")
    b.plotly_chart(chart(px.bar(p.sort_values("revenue"),x="revenue",y="product_name",orientation="h",title="Top 10 Products by Revenue")),use_container_width=True)
    st.markdown('<div class="section">Detailed output table</div>', unsafe_allow_html=True)
    st.dataframe(s.sort_values("revenue",ascending=False),use_container_width=True,hide_index=True)

else:
    st.markdown('<div class="section">Regional outputs</div>', unsafe_allow_html=True)
    r=X.groupby("region",as_index=False).agg(revenue=("line_total","sum"),profit=("line_profit","sum"),orders=("order_id","nunique"))
    r["margin"]=r.profit/r.revenue
    a,b=st.columns(2)
    fig=go.Figure([go.Bar(x=r.region,y=r.revenue,name="Revenue"),go.Scatter(x=r.region,y=r.profit,name="Profit",yaxis="y2")])
    fig.update_layout(title="Regional Revenue vs Profit",yaxis2=dict(overlaying="y",side="right"))
    a.plotly_chart(chart(fig),use_container_width=True)
    ship=X.groupby("ship_mode",as_index=False).agg(orders=("order_id","nunique"),avg_days=("delivery_days","mean"))
    b.plotly_chart(chart(px.bar(ship,x="ship_mode",y="orders",title="Orders by Shipping Mode")),use_container_width=True)
    state=X.groupby("state",as_index=False).line_total.sum().nlargest(10,"line_total")
    st.plotly_chart(chart(px.bar(state.sort_values("line_total"),x="line_total",y="state",orientation="h",title="Top 10 States by Revenue")),use_container_width=True)

st.divider()
st.markdown('<div class="small">Data source: deterministic synthetic e-commerce dataset (seed 42). Dashboard calculations use Delivered + Shipped transactions.</div>', unsafe_allow_html=True)
