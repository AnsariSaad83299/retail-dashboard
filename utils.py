import psycopg2
import pandas as pd
import streamlit as st

# --- Database Connection ---

# Local Connection
# def get_connection():
#     """Establishes and returns a new database connection."""
#     return psycopg2.connect(
#         host="localhost",
#         database="dmql-project-retail-data",  # <-- change this
#         user="postgres",            # <-- change this
#         password="pgsql"         # <-- change this
#     )

# Remote railway connection

def get_connection():
    return psycopg2.connect(
        host="interchange.proxy.rlwy.net",       # <-- your Railway host
        database="railway",                      # <-- your Railway database name
        user="postgres",                         # <-- your Railway username
        password="pOcmcFvgwATZHrLtHMQclpHUezoZwRQw",   # <-- your Railway password
        port=47582                               # <-- your Railway port
    )


# --- Run SQL Query ---
@st.cache_data(show_spinner=False)
def run_query(query):
    """Executes a SQL query and returns results as a DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- General Utilities (Optional) ---
def format_currency(value):
    """Formats a number as currency."""
    return f"${value:,.2f}"

def format_date(date):
    """Formats a date nicely."""
    return date.strftime("%d %b %Y")
