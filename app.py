import time
import os
import pyodbc
import pandas as pd
import plotly.express as px
import streamlit as st
from db_connection import get_db_connection
from dotenv import load_dotenv

# Load environment variables from sql_env file
load_dotenv(dotenv_path="sql_env")

# Set Streamlit page config and styling
st.set_page_config(page_title="Restaurant Dashboard", layout="wide")
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            margin-top: -60px;
        }
        [data-testid="stAppViewContainer"] {
            padding-top: 0px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("<h1 class='title'>Pizza House Dashboard</h1>", unsafe_allow_html=True)

# -------------------------
# Data fetching functions
# -------------------------

@st.cache_data(ttl=5)
def get_city_data():
    query = """
        SELECT delivery_city, COUNT(*) AS city_count
        FROM [Restaurant].[dbo].[address]
        GROUP BY delivery_city
        ORDER BY city_count DESC;
    """
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=5)
def get_food_data():
    query = """
        SELECT i.item_name, SUM(o.quantity) AS total_sold
        FROM [Restaurant].[dbo].[order] o
        JOIN [Restaurant].[dbo].[item] i ON o.item_id = i.item_id
        GROUP BY i.item_name
        ORDER BY total_sold DESC;
    """
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=5)
def get_delivery_data():
    query = """
        SELECT ca.delivery_city,
               SUM(o.quantity * i.price) AS total_revenue,
               COUNT(o.add_id) AS delivery_count
        FROM [Restaurant].[dbo].[order] o
        JOIN [Restaurant].[dbo].[item] i ON o.item_id = i.item_id
        JOIN [Restaurant].[dbo].[address] ca ON o.cust_id = ca.add_id
        WHERE o.delivery = 1
        GROUP BY ca.delivery_city;
    """
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=5)
def get_average():
    query = """
        SELECT AVG(o.quantity * i.price) AS average_order_value
        FROM [Restaurant].[dbo].[order] o
        JOIN [Restaurant].[dbo].[item] i ON o.item_id = i.item_id;
    """
    with get_db_connection() as conn:
        df = pd.read_sql(query, conn)
    return df["average_order_value"].iloc[0]

@st.cache_data(ttl=5)
def get_totalRevenue():
    query = """
        SELECT SUM(o.quantity * i.price) AS total_revenue
        FROM [Restaurant].[dbo].[order] o
        JOIN [Restaurant].[dbo].[item] i ON o.item_id = i.item_id;
    """
    with get_db_connection() as conn:
        df = pd.read_sql(query, conn)
    return df["total_revenue"].iloc[0]

@st.cache_data(ttl=5)
def get_totalcustomer():
    query = "SELECT COUNT(*) AS customer_count FROM [Restaurant].[dbo].[customers];"
    with get_db_connection() as conn:
        df = pd.read_sql(query, conn)
    return df["customer_count"].iloc[0]

@st.cache_data(ttl=5)
def get_sales_per_day():
    query = """
        SELECT CONVERT(date, o.created_at) AS order_date,
               SUM(o.quantity * i.price) AS sales
        FROM [Restaurant].[dbo].[order] o
        JOIN [Restaurant].[dbo].[item] i ON o.item_id = i.item_id
        GROUP BY CONVERT(date, o.created_at)
        ORDER BY order_date;
    """
    with get_db_connection() as conn:
        return pd.read_sql(query, conn)

@st.cache_data(ttl=60)
def get_rating_data():
    query = """
        SELECT DATEPART(year, created_at) AS year,
               DATEPART(week, created_at) AS week,
               AVG(CASE WHEN rating > 0 THEN rating END) AS avg_rating
        FROM [Restaurant].[dbo].[review]
        WHERE rating > 0
        GROUP BY DATEPART(year, created_at), DATEPART(week, created_at)
        ORDER BY year, week;
    """
    with get_db_connection() as conn:
        df = pd.read_sql(query, conn)
    # Add a color column based on average rating
    df["color"] = df["avg_rating"].apply(lambda x: "red" if x < 5 else "yellow" if x < 7 else "green")
    return df

# -------------------------
# Fetch data from database
# -------------------------
df_city = get_city_data()
df_food = get_food_data()
df_delivery = get_delivery_data()
df_average = get_average()
df_totalRevenue = get_totalRevenue()
df_totalcustomer = get_totalcustomer()
df_daily_sales = get_sales_per_day()
df_rating = get_rating_data()

# Display key metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Total Revenue", f"${df_totalRevenue:,.2f}")
with col2:
    st.metric("Total Delivery Orders", f"{df_delivery['delivery_count'].sum():,.0f}")
with col3:
    st.metric("Total Customers", f"{df_totalcustomer}")
with col4:
    st.metric("Average Per Ticket", f"${df_average:,.2f}")
with col5:
    gross_margin = ((df_totalRevenue - (0.733 * df_totalRevenue)) / df_totalRevenue) * 100
    st.metric("Gross Margin", f"{gross_margin:,.2f}%")
with col6:
    net_profit = ((df_totalRevenue - (0.862 * df_totalRevenue)) / df_totalRevenue) * 100
    st.metric("Net Profit", f"{net_profit:,.2f}%")

# -------------------------
# Create visualizations
# -------------------------

# Split into two columns for city and food charts
col_left, col_right = st.columns(2)
with col_left:
    fig_city = px.bar(df_city, x="delivery_city", y="city_count", title="Number of Customers by City", template="seaborn")
    fig_city.update_layout(title_x=0.4)
    st.plotly_chart(fig_city, use_container_width=True)
with col_right:
    fig_food = px.pie(df_food, values="total_sold", names="item_name", title="Total Sold Items by Food Category", template="seaborn")
    fig_food.update_layout(title_x=0.4)
    st.plotly_chart(fig_food, use_container_width=True)

# Create three columns for additional charts
col_a, col_b, col_c = st.columns(3)
with col_a:
    fig_delivery = px.bar(
        df_delivery, 
        x="delivery_city", 
        y=["total_revenue", "delivery_count"],
        title="Delivery Orders and Revenue by City",
        template="seaborn",
        labels={"delivery_city": "City", "total_revenue": "Total Revenue", "delivery_count": "Delivery Count"},
        barmode="group"
    )
    fig_delivery.update_layout(title_x=0.3)
    st.plotly_chart(fig_delivery, use_container_width=True)

with col_b:
    fig_rating = px.bar(
        df_rating, 
        x="week", 
        y="avg_rating", 
        title="Average Rating Trends", 
        template="seaborn",
        color="color", 
        color_discrete_map={"red": "red", "yellow": "yellow", "green": "green"}
    )
    fig_rating.update_layout(title_x=0.4)
    st.plotly_chart(fig_rating, use_container_width=True)

with col_c:
    fig_daily_sales = px.line(df_daily_sales, x="order_date", y="sales", title="Sales Trends", template="seaborn")
    fig_daily_sales.update_layout(title_x=0.4)
    st.plotly_chart(fig_daily_sales, use_container_width=True)

# Rerun the app after 5 seconds
time.sleep(5)
st.rerun()
