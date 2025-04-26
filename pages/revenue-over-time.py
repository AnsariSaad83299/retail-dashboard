import streamlit as st
import plotly.express as px
from utils import run_query

st.title("📈 Total Revenue Over Time")

# --- Step 1: Get all store locations ---
stores_df = run_query("SELECT DISTINCT location FROM stores;")
store_options = ["All Stores"] + stores_df["location"].tolist()

# --- Step 2: Create a dropdown ---
selected_store = st.selectbox("Select Store Location:", options=store_options)

# --- Step 3: Query data based on selection ---
if selected_store == "All Stores":
    df = run_query("""
        SELECT openingdate AS date, totalrevenue, location
        FROM stores
        ORDER BY openingdate;
    """)
else:
    df = run_query(f"""
        SELECT openingdate AS date, totalrevenue, location
        FROM stores
        WHERE location = '{selected_store}'
        ORDER BY openingdate;
    """)

# --- Step 4: Plot the results ---
fig = px.line(
    df,
    x='date',
    y='totalrevenue',
    color='location' if selected_store == "All Stores" else None,
    title=f"Revenue Over Time - {selected_store}"
)

st.plotly_chart(fig)

# --- Optional: Show raw data ---
with st.expander("See Raw Data"):
    st.dataframe(df)
