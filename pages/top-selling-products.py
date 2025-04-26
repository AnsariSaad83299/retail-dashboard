import streamlit as st
import plotly.express as px
from utils import run_query

st.title("🏆 Top Selling Products")

# --- Step 1: Fetch all available product categories ---
categories_df = run_query("SELECT DISTINCT category FROM products;")
category_options = categories_df["category"].tolist()

# --- Step 2: Multiselect categories ---
selected_categories = st.multiselect(
    "Select Product Categories:",
    options=category_options,
    default=category_options  # by default, select all
)

# --- Step 3: Choose number of top products to show ---
top_n = st.slider("Select how many top products to display:", min_value=5, max_value=50, value=10)

# --- Step 4: Build dynamic SQL Query based on selection ---
query = """
    SELECT p.name, SUM(od.quantity) as total_sold
    FROM order_details od
    JOIN products p ON od.productid = p.productid
"""
if selected_categories:
    category_filter = ",".join(f"'{cat}'" for cat in selected_categories)
    query += f" WHERE p.category IN ({category_filter}) "

query += """
    GROUP BY p.name
    ORDER BY total_sold DESC
    LIMIT {}
""".format(top_n)

# --- Step 5: Run Query and Plot ---
df = run_query(query)

fig = px.bar(
    df,
    x='name',
    y='total_sold',
    title=f"Top {top_n} Selling Products",
    labels={"name": "Product Name", "total_sold": "Units Sold"}
)
fig.update_layout(xaxis_tickangle=-45)

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
