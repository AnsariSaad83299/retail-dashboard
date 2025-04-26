import streamlit as st
import plotly.express as px
from utils import run_query

st.title("🛒 Order Status Distribution")

# --- Step 1: Fetch earliest and latest order dates ---
date_df = run_query("SELECT MIN(orderdate) as min_date, MAX(orderdate) as max_date FROM orders;")
min_date = date_df['min_date'][0]
max_date = date_df['max_date'][0]

# --- Step 2: Create a date range picker ---
start_date, end_date = st.date_input(
    "Select Order Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --- Step 3: Build query based on selected date range ---
query = f"""
    SELECT status, COUNT(*) as num_orders
    FROM orders
    WHERE orderdate BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY status
    ORDER BY num_orders DESC;
"""

# --- Step 4: Run query and plot ---
df = run_query(query)

fig = px.pie(
    df,
    names='status',
    values='num_orders',
    title="Order Status Distribution",
    hole=0.4  # donut chart style
)

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
