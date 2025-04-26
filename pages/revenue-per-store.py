import streamlit as st
import plotly.express as px
from utils import run_query, format_currency

st.title("🏬 Revenue per Store")

# --- Step 1: Fetch available store locations ---
stores_df = run_query("SELECT DISTINCT location FROM stores;")
store_options = stores_df["location"].tolist()

# --- Step 2: Multiselect for picking specific stores ---
selected_stores = st.multiselect(
    "Select Store(s):",
    options=store_options,
    default=store_options  # By default, show all stores
)

# --- Step 3: Choose sort order ---
sort_order = st.radio(
    "Sort by Revenue:",
    ["Descending", "Ascending"],
    horizontal=True
)

# --- Step 4: Build dynamic query based on selection ---
query = """
    SELECT location, totalrevenue
    FROM stores
"""
if selected_stores:
    store_filter = ",".join(f"'{store}'" for store in selected_stores)
    query += f" WHERE location IN ({store_filter}) "

query += " ORDER BY totalrevenue DESC;" if sort_order == "Descending" else " ORDER BY totalrevenue ASC;"

# --- Step 5: Run query and plot ---
df = run_query(query)

fig = px.bar(
    df,
    x='location',
    y='totalrevenue',
    title=f"Store Revenue ({sort_order})",
    labels={"location": "Store Location", "totalrevenue": "Total Revenue"},
    text_auto=True
)
fig.update_layout(xaxis_tickangle=-45)
fig.update_traces(
    text=df['totalrevenue'],              # setting text values
    texttemplate='%{text:$,.2f}',          # formatting text
    textposition='outside'                 # positioning text outside bars
)
st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    df["Formatted Revenue"] = df["totalrevenue"].apply(format_currency)
    st.dataframe(df)
