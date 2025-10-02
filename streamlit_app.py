import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
   page_title="Customer Segmentation",
   page_icon="📊",
   layout="wide",
   initial_sidebar_state="expanded",
)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/andrianusalvien/Customer-Segmentation/refs/heads/main/superstore_dataset%20-%20segmentation%20-%20superstore.csv"
    df = pd.read_csv(url, parse_dates=["order_date"])
    return df

df = load_data()
st.title("📊 Customer Segmentation with RFM Analysis")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filters")

# Date filter
min_date, max_date = df["order_date"].min(), df["order_date"].max()
date_range = st.sidebar.date_input("Filter by Date Range", [min_date, max_date])
if isinstance(date_range, list) and len(date_range) == 2:
    df = df[(df["order_date"] >= pd.to_datetime(date_range[0])) & 
            (df["order_date"] <= pd.to_datetime(date_range[1]))]

# --- PREPARE RFM DATA ---
latest_date = df["order_date"].max()

rfm = df.groupby("customer_id").agg({
    "order_date": lambda x: (latest_date - x.max()).days,
    "order_id": "nunique",
    "sales": "sum",
    "profit": "sum"
}).reset_index()

rfm.columns = ["customer_id", "Recency", "Frequency", "Monetary", "Profit"]

# --- RFM SCORES ---
rfm["R_score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])  
rfm["F_score"] = pd.qcut(rfm["Frequency"], 4, labels=[1,2,3,4])
rfm["M_score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

rfm["RFM_Score"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)

# --- SEGMENTATION RULES ---
def segment_customer(row):
    r, f, m = int(row["R_score"]), int(row["F_score"]), int(row["M_score"])
    if r >= 3 and f >= 3 and m >= 3:
        return "Champion"
    elif r >= 3 and f >= 2:
        return "Loyal Customer"
    elif r == 2 and f >= 2:
        return "Potential Loyalist"
    elif r >= 3 and f == 1:
        return "Recent Customer"
    elif r == 2 and f == 1:
        return "Promising"
    elif r == 1 and f >= 3:
        return "At Risk"
    elif r == 1 and f == 2:
        return "Need Attention"
    else:
        return "Hibernating"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# --- MERGE with Customer Info ---
cust_info = df[["customer_id","state"]].drop_duplicates()
rfm = rfm.merge(cust_info, on="customer_id", how="left")

# --- FILTER STATE ---
states = sorted(df["state"].unique())
selected_state = st.sidebar.selectbox("Filter by State", ["All"] + states)

if selected_state != "All":
    rfm = rfm[rfm["state"] == selected_state]

# --- FILTER SEGMENT ---
segments = sorted(rfm["Segment"].unique())
selected_segment = st.sidebar.multiselect("Filter by Segment", segments, default=segments)

if selected_segment:
    rfm = rfm[rfm["Segment"].isin(selected_segment)]

# --- SUMMARY METRICS ---
total_customers = df["customer_id"].count()
total_sales = df["sales"].sum()

col1, col2 = st.columns(2)
col1.metric("👥 Total Customers", f"{total_customers:,}")
col2.metric("💰 Total Sales", f"${total_sales:,.2f}")



# --- DISTRIBUSI SEGMENTASI ---
st.subheader("Customer Segmentation Distribution")
seg_counts = rfm["Segment"].value_counts().reset_index()
if not seg_counts.empty:
    fig_pie = px.pie(seg_counts, values="count", names="Segment")
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("No data available for selected filters.")

# --- PROFIT BY SEGMENT ---
st.subheader("Profit by Customer Segment")
profit_seg = rfm.groupby("Segment")["Profit"].sum().reset_index().sort_values("Profit", ascending=False)
if not profit_seg.empty:
    fig_bar = px.bar(profit_seg, x="Segment", y="Profit", color="Segment")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- DISTRIBUTION PER CATEGORY ---
st.subheader("Distribution per Product Category")
cat_dist = df.groupby("category")["sales"].sum().reset_index()
if not cat_dist.empty:
    fig_cat = px.pie(cat_dist, values="sales", names="category")
    st.plotly_chart(fig_cat, use_container_width=True)

# --- PERSEBARAN CUSTOMER PER WAKTU ---
st.subheader("Customer Activity Over Time")
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
cust_time = df.groupby("order_month")["customer_id"].nunique().reset_index(name="unique_customers")
if not cust_time.empty:
    fig_time = px.line(cust_time, x="order_month", y="unique_customers",
                       title="Unique Customers Over Time", markers=True)
    st.plotly_chart(fig_time, use_container_width=True)
    

# --- DISPLAY DATA ---
st.subheader("RFM Table (Filtered)")
st.dataframe(rfm.head(20))

# --- SEGMENT SUMMARY ---
st.subheader("Segment Summary")
segment_summary = rfm.groupby("Segment").agg({
    "customer_id": "count",
    "Recency": "mean",
    "Frequency": "mean",
    "Monetary": "mean",
    "Profit": "mean"
}).rename(columns={"customer_id": "Total_Customer"}).sort_values("Total_Customer", ascending=False)

st.dataframe(segment_summary)
