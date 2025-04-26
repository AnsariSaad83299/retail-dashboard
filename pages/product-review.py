import streamlit as st
import plotly.express as px
from utils import run_query

st.title("⭐ Average Product Ratings")

# --- Step 1: Fetch all available categories ---
categories_df = run_query("SELECT DISTINCT category FROM products;")
category_options = categories_df["category"].tolist()

# --- Step 2: Multiselect to pick one or more categories ---
selected_categories = st.multiselect(
    "Select Product Categories:",
    options=category_options,
    default=category_options  # default: all categories selected
)

# --- Step 3: Slider for minimum rating filter ---
min_rating = st.slider(
    "Minimum Average Rating:",
    min_value=1,
    max_value=5,
    value=1,
    step=1
)

# --- Step 4: Build dynamic query ---
query = """
    SELECT p.name, p.category, ROUND(AVG(r.rating),2) as avg_rating, COUNT(r.reviewid) as num_reviews
    FROM reviews r
    JOIN products p ON r.productid = p.productid
"""
if selected_categories:
    category_filter = ",".join(f"'{cat}'" for cat in selected_categories)
    query += f" WHERE p.category IN ({category_filter}) "

query += """
    GROUP BY p.name, p.category
    HAVING ROUND(AVG(r.rating),2) >= {}
    LIMIT 50
""".format(min_rating)

# --- Step 5: Run query and plot ---
df = run_query(query)

fig = px.bar(
    df,
    x='name',
    y='avg_rating',
    color='category',
    title=f"Top Rated Products (Filtered by Categories and Rating)",
    labels={"name": "Product Name", "avg_rating": "Average Rating"},
    hover_data=['num_reviews']
)

fig.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 5])

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
