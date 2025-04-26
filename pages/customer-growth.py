import streamlit as st
import plotly.express as px
from utils import run_query

st.title("📈 Customer Growth Over Time")

# --- Step 1: Get the earliest and latest join dates ---
date_df = run_query("SELECT MIN(joindate) as min_date, MAX(joindate) as max_date FROM customers;")
min_date = date_df['min_date'][0]
max_date = date_df['max_date'][0]

# --- Step 2: Create a date range picker ---
start_date, end_date = st.date_input(
    "Select Join Date Range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --- Step 3: Choose aggregation level (Day, Month, Year) ---
agg_level = st.radio(
    "Select Aggregation Level:",
    ["Daily", "Monthly", "Yearly"],
    horizontal=True
)

# --- Step 4: Build query based on selected aggregation ---
if agg_level == "Daily":
    date_format = "joindate"
elif agg_level == "Monthly":
    date_format = "TO_CHAR(joindate, 'YYYY-MM')"
elif agg_level == "Yearly":
    date_format = "TO_CHAR(joindate, 'YYYY')"

query = f"""
    SELECT {date_format} as period, COUNT(*) as new_customers
    FROM customers
    WHERE joindate BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY period
    ORDER BY period;
"""

# --- Step 5: Run the query and plot ---
df = run_query(query)

fig = px.line(
    df,
    x='period',
    y='new_customers',
    title=f"Customer Growth ({agg_level})",
    labels={"period": f"Join Date ({agg_level})", "new_customers": "Number of New Customers"},
    markers=True
)

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
