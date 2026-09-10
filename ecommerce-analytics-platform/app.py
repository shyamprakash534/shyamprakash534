import streamlit as st
import pandas as pd, numpy as np
import plotly.express as px, plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title='E-Commerce Executive Analytics', page_icon='📊', layout='wide')
BASE=Path(__file__).parent; DATA=BASE/'data'; CLEAN=DATA/'cleaned'

def build_data():
    rng=np.random.default_rng(42); CLEAN.mkdir(parents=True,exist_ok=True)
    geo=pd.DataFrame([
        ['10001','New York','New York','East'],['19104','Philadelphia','Pennsylvania','East'],['02138','Boston','Massachusetts','East'],
        ['90001','Los Angeles','California','West'],['94102','San Francisco','California','West'],['98101','Seattle','Washington','West'],
        ['60601','Chicago','Illinois','Central'],['48201','Detroit','Michigan','Central'],['75201','Dallas','Texas','Central'],
        ['77001','Houston','Texas','Central'],['30301','Atlanta','Georgia','South'],['33101','Miami','Florida','South'],
        ['27601','Raleigh','North Carolina','South'],['80202','Denver','Colorado','West'],['85001','Phoenix','Arizona','West']],
        columns=['postal_code','city','state','region'])
    cats=pd.DataFrame([
        ['Technology','Phones',.22],['Technology','Accessories',.35],['Technology','Copiers',.40],['Technology','Machines',.05],
        ['Furniture','Chairs',.18],['Furniture','Tables',-.08],['Furniture','Bookcases',.12],['Furniture','Furnishings',.25],
        ['Office Supplies','Storage',.20],['Office Supplies','Binders',.32],['Office Supplies','Paper',.42],['Office Supplies','Art',.30],['Office Supplies','Appliances',.28],['Office Supplies','Envelopes',.38]],
        columns=['category','sub_category','target_margin'])
    products=[]; pid=1001
    for _,c in cats.iterrows():
        for j in range(4):
            price=float(rng.uniform(450,1800) if c.sub_category in ['Copiers','Machines','Tables'] else rng.uniform(30,600))
            if c.sub_category in ['Binders','Paper','Art','Envelopes']: price=float(rng.uniform(8,45))
            cost=price*(1-float(c.target_margin+rng.uniform(-.05,.05)))
            products.append([f'PRD-{pid}',f'{c.sub_category} Product {j+1}',c.category,c.sub_category,round(price,2),round(max(cost,price*.4),2)]); pid+=1
    products=pd.DataFrame(products,columns=['product_id','product_name','category','sub_category','base_price','cost_price'])
    segs=rng.choice(['Consumer','Corporate','Home Office'],1250,p=[.52,.30,.18]); geo_pick=rng.integers(0,len(geo),1250)
    customers=pd.DataFrame({'customer_id':[f'CUST-{i:04d}' for i in range(1,1251)],'customer_segment':segs,'postal_code':geo.iloc[geo_pick].postal_code.values})
    orders=[]; items=[]; oid=10001; iid=50001
    for _,cu in customers.iterrows():
        n=int(rng.choice([1,2,3,4,5,6,7],p=[.45,.14,.14,.10,.07,.06,.04]))
        for _ in range(n):
            d=pd.Timestamp('2022-01-01')+pd.Timedelta(days=int(rng.integers(0,730))); mode=rng.choice(['Standard Class','Second Class','First Class','Same Day'],p=[.59,.20,.15,.06]); delay={'Standard Class':5,'Second Class':3,'First Class':2,'Same Day':0}[mode]+int(rng.integers(0,2))
            status=rng.choice(['Delivered','Shipped','Cancelled','Returned'],p=[.89,.04,.04,.03]); order=f'ORD-{oid}'; oid+=1
            orders.append([order,cu.customer_id,d,d+pd.Timedelta(days=delay),mode,status,cu.postal_code,cu.customer_segment])
            for pr in products.iloc[rng.choice(len(products),size=int(rng.choice([1,2,3],p=[.5,.35,.15])),replace=False)].itertuples():
                q=int(rng.choice([1,2,3,4,5],p=[.55,.25,.12,.05,.03]))
                if pr.sub_category=='Tables': disc=float(rng.choice([.15,.25,.35,.45,.55],p=[.1,.25,.3,.25,.1]))
                elif pr.sub_category=='Machines': disc=float(rng.choice([.1,.2,.3,.4],p=[.2,.4,.3,.1]))
                else: disc=float(rng.choice([0,.05,.1,.15,.2],p=[.45,.25,.15,.1,.05]))
                gross=q*pr.base_price; net=gross*(1-disc); cost=q*pr.cost_price
                items.append([f'ITEM-{iid}',order,pr.product_id,q,pr.base_price,disc,net,cost,net-cost]); iid+=1
    orders=pd.DataFrame(orders,columns=['order_id','customer_id','order_date','ship_date','ship_mode','order_status','postal_code','customer_segment'])
    items=pd.DataFrame(items,columns=['order_item_id','order_id','product_id','quantity','unit_price','discount_pct','line_total','line_cost','line_profit'])
    for df,name in [(geo,'geography'),(cats,'categories'),(products,'products'),(customers,'customers'),(orders,'orders'),(items,'order_items')]: df.to_csv(CLEAN/f'{name}.csv',index=False)

def load():
    if not (CLEAN/'orders.csv').exists(): build_data()
    g=pd.read_csv(CLEAN/'geography.csv'); p=pd.read_csv(CLEAN/'products.csv'); o=pd.read_csv(CLEAN/'orders.csv',parse_dates=['order_date','ship_date']); i=pd.read_csv(CLEAN/'order_items.csv')
    f=i.merge(o,on='order_id').merge(p,on='product_id').merge(g,on='postal_code'); f['gross_line']=f.quantity*f.unit_price; f['discount_amount']=f.gross_line-f.line_total; f['delivery_days']=(f.ship_date-f.order_date).dt.days; f['month']=f.order_date.dt.to_period('M').dt.to_timestamp(); return f
F=load(); F=F[F.order_status.isin(['Delivered','Shipped'])].copy()

def money(x): return f'${x/1e6:.2f}M' if abs(x)>=1e6 else f'${x/1e3:.1f}K'
def pct(x): return f'{x*100:.2f}%'
def base(fig,h=350):
    fig.update_layout(template='plotly_dark',height=h,margin=dict(l=10,r=10,t=50,b=10),paper_bgcolor='#151f31',plot_bgcolor='#151f31',font_color='#dbe5f3'); return fig
st.markdown('''<style>.stApp{background:#0b1220}.block-container{max-width:1500px}.k{background:#151f31;border:1px solid #2a3a57;border-radius:14px;padding:15px}.kv{font-size:27px;font-weight:750}.ks{font-size:11px;color:#8fa0b8}</style>''',unsafe_allow_html=True)
st.sidebar.title('Executive Dashboard'); st.sidebar.caption('E-Commerce Sales, Customer & Profitability Analytics')
region=st.sidebar.selectbox('Region',['All']+sorted(F.region.unique())); category=st.sidebar.selectbox('Category',['All']+sorted(F.category.unique())); segment=st.sidebar.selectbox('Segment',['All']+sorted(F.customer_segment.unique()))
start=st.sidebar.date_input('Start date',F.order_date.min().date()); end=st.sidebar.date_input('End date',F.order_date.max().date())
page=st.sidebar.radio('Page',['1. Executive Overview','2. Sales & Profitability','3. Customer Analytics','4. Product & Category','5. Regional Performance'],index=1)
X=F[(F.order_date.dt.date>=start)&(F.order_date.dt.date<=end)].copy()
if region!='All': X=X[X.region==region]
if category!='All': X=X[X.category==category]
if segment!='All': X=X[X.customer_segment==segment]
net=X.line_total.sum(); profit=X.line_profit.sum(); gross=X.gross_line.sum(); orders=X.order_id.nunique(); customers=X.customer_id.nunique(); margin=profit/net if net else 0; disc=(gross-net)/gross if gross else 0; leak=-X.loc[X.discount_pct>.20,'line_profit'].sum()
cols=st.columns(4)
for col,label,val,sub in zip(cols,['YTD Net Revenue','YTD Net Profit','Profit Margin','Margin Leakage (>20% Disc)'],[money(net),money(profit),pct(margin),money(leak)],[f'Gross Sales {money(gross)}',f'Orders {orders:,}',f'Discount Rate {pct(disc)}',f'Customers {customers:,}']): col.markdown(f'<div class="k"><div>{label}</div><div class="kv">{val}</div><div class="ks">{sub}</div></div>',unsafe_allow_html=True)
if page== '1. Executive Overview':
    st.title('Executive Overview'); m=X.groupby('month',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum')); fig=go.Figure([go.Scatter(x=m.month,y=m.revenue,name='Revenue'),go.Scatter(x=m.month,y=m.profit,name='Profit',yaxis='y2')]); fig.update_layout(title='Monthly Revenue & Profit Trajectory',yaxis2=dict(overlaying='y',side='right')); st.plotly_chart(base(fig,420),use_container_width=True)
    a,b=st.columns(2); a.plotly_chart(base(px.bar(X.groupby('customer_segment',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum')),x='customer_segment',y=['revenue','profit'],barmode='group',title='Segment Revenue vs Profit')),use_container_width=True); b.plotly_chart(base(px.bar(X.groupby('region',as_index=False).line_total.sum(),x='region',y='line_total',title='Regional Revenue')),use_container_width=True)
elif page=='2. Sales & Profitability':
    st.title('Sales & Profitability Deep Dive'); m=X.groupby('month',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum')); m['mom']=m.revenue.pct_change()*100; m['cum_rev']=m.revenue.cumsum(); m['cum_profit']=m.profit.cumsum(); a,b=st.columns(2); a.plotly_chart(base(px.bar(m,x='month',y='mom',title='Monthly MoM Revenue Growth (%)')),use_container_width=True); fig=go.Figure([go.Scatter(x=m.month,y=m.cum_rev,name='Cumulative Revenue'),go.Scatter(x=m.month,y=m.cum_profit,name='Cumulative Profit',yaxis='y2')]); fig.update_layout(title='Cumulative Revenue & Profit Trajectory',yaxis2=dict(overlaying='y',side='right')); b.plotly_chart(base(fig),use_container_width=True); s=X.groupby('sub_category',as_index=False).agg(gross=('gross_line','sum'),revenue=('line_total','sum'),profit=('line_profit','sum')); s['discount']=1-s.revenue/s.gross; s['margin']=s.profit/s.revenue; st.plotly_chart(base(px.scatter(s,x='discount',y='margin',size='gross',hover_name='sub_category',title='Discount % vs Profit Margin')),use_container_width=True)
elif page=='3. Customer Analytics':
    st.title('Customer Segmentation & Lifetime Value'); s=X.groupby('customer_segment',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum'),customers=('customer_id','nunique')); s['margin']=s.profit/s.revenue; a,b=st.columns(2); a.plotly_chart(base(px.bar(s,x='customer_segment',y=['revenue','profit'],barmode='group',title='Customer Segment Performance')),use_container_width=True); cu=X.groupby('customer_id').agg(revenue=('line_total','sum'),orders=('order_id','nunique')).sort_values('revenue',ascending=False).reset_index(); cu['decile']=pd.qcut(np.arange(1,len(cu)+1),10,labels=[f'D{i}' for i in range(1,11)]); d=cu.groupby('decile',observed=False).revenue.sum().reset_index(); d['share']=100*d.revenue/d.revenue.sum(); b.plotly_chart(base(px.bar(d,x='decile',y='share',title='Pareto Decile Spend Distribution')),use_container_width=True); freq=X.groupby('customer_id').order_id.nunique().value_counts().sort_index().reset_index(); freq.columns=['orders','customers']; st.plotly_chart(base(px.bar(freq,x='orders',y='customers',title='Buyer Frequency & Retention Distribution')),use_container_width=True)
elif page=='4. Product & Category':
    st.title('Product & Category Profitability'); s=X.groupby(['category','sub_category'],as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum'),gross=('gross_line','sum')); s['margin']=s.profit/s.revenue; s['discount']=1-s.revenue/s.gross; a,b=st.columns(2); a.plotly_chart(base(px.bar(s.sort_values('profit'),x='profit',y='sub_category',orientation='h',title='Sub-Category Net Profit / Loss')),use_container_width=True); p=X.groupby('product_name',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum')).nlargest(10,'revenue'); b.plotly_chart(base(px.bar(p.sort_values('revenue'),x='revenue',y='product_name',orientation='h',title='Top 10 Products by Revenue')),use_container_width=True); st.dataframe(s.sort_values('revenue',ascending=False),use_container_width=True,hide_index=True)
else:
    st.title('Regional & Geographic Performance'); r=X.groupby('region',as_index=False).agg(revenue=('line_total','sum'),profit=('line_profit','sum'),orders=('order_id','nunique')); r['margin']=r.profit/r.revenue; a,b=st.columns(2); fig=go.Figure([go.Bar(x=r.region,y=r.revenue,name='Revenue'),go.Scatter(x=r.region,y=r.profit,name='Profit',yaxis='y2')]); fig.update_layout(title='Regional Financial Comparison: Revenue vs Profit',yaxis2=dict(overlaying='y',side='right')); a.plotly_chart(base(fig),use_container_width=True); ship=X.groupby('ship_mode',as_index=False).agg(orders=('order_id','nunique'),avg_days=('delivery_days','mean')); b.plotly_chart(base(px.bar(ship,x='ship_mode',y='orders',title='Logistics SLA & Shipping Mode Distribution')),use_container_width=True); state=X.groupby('state',as_index=False).line_total.sum().nlargest(10,'line_total'); st.plotly_chart(base(px.bar(state.sort_values('line_total'),x='line_total',y='state',orientation='h',title='Top 10 States by Revenue Contribution')),use_container_width=True)
