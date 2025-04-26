import streamlit as st
import plotly.express as px
from utils import run_query

st.title("🏬 Inventory Levels per Store")

# --- Step 1: Fetch all available store locations ---
stores_df = run_query("SELECT DISTINCT location FROM stores;")
store_options = stores_df["location"].tolist()

# --- Step 2: Multiselect to pick one or multiple stores ---
selected_stores = st.multiselect(
    "Select Store(s):",
    options=store_options,
    default=store_options  # by default show all stores
)

# --- Step 3: Build dynamic query based on selection ---
query = """
    SELECT s.location, SUM(i.quantity) as total_inventory
    FROM inventory i
    JOIN stores s ON i.storeid = s.storeid
"""
if selected_stores:
    store_filter = ",".join(f"'{store}'" for store in selected_stores)
    query += f" WHERE s.location IN ({store_filter}) "

query += """
    GROUP BY s.location
    ORDER BY total_inventory DESC;
"""

# --- Step 4: Run the query and plot ---
df = run_query(query)

fig = px.bar(
    df,
    x='location',
    y='total_inventory',
    title="Inventory Levels by Store",
    labels={"location": "Store Location", "total_inventory": "Total Items in Inventory"},
    text_auto=True
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
