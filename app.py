import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Food Wastage Dashboard", layout="wide")

st.title("🍽️ Local Food Wastage Management Dashboard")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    providers = pd.read_csv("data/providers_data.csv")
    receivers = pd.read_csv("data/receivers_data.csv")
    food = pd.read_csv("data/food_listings_data.csv")
    claims = pd.read_csv("data/claims_data.csv")
    return providers, receivers, food, claims

providers, receivers, food, claims = load_data()

# ---------------------------
# Merge Data (IMPORTANT STEP)
# ---------------------------
df = food.merge(providers, on="provider_id", how="left")
df = df.merge(claims, on="food_id", how="left")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.header("🔍 Filters")

city = st.sidebar.selectbox("Select City", ["All"] + list(df["city"].dropna().unique()))
food_type = st.sidebar.selectbox("Food Type", ["All"] + list(df["food_type"].dropna().unique()))
meal_type = st.sidebar.selectbox("Meal Type", ["All"] + list(df["meal_type"].dropna().unique()))

# Apply filters
filtered_df = df.copy()

if city != "All":
    filtered_df = filtered_df[filtered_df["city"] == city]

if food_type != "All":
    filtered_df = filtered_df[filtered_df["food_type"] == food_type]

if meal_type != "All":
    filtered_df = filtered_df[filtered_df["meal_type"] == meal_type]

# ---------------------------
# KPI METRICS
# ---------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Food Items", len(filtered_df))
col2.metric("Total Quantity", int(filtered_df["quantity"].sum()))
col3.metric("Total Providers", filtered_df["provider_id"].nunique())
col4.metric("Total Claims", filtered_df["claim_id"].nunique())

# ---------------------------
# CHARTS
# ---------------------------

st.subheader("📈 Analysis")

col1, col2 = st.columns(2)

# Food Type Distribution
food_type_chart = px.pie(filtered_df, names="food_type", title="Food Type Distribution")
col1.plotly_chart(food_type_chart, use_container_width=True)

# Meal Type Distribution
meal_chart = px.bar(filtered_df, x="meal_type", title="Meal Type Count")
col2.plotly_chart(meal_chart, use_container_width=True)

# ---------------------------
# CLAIM STATUS ANALYSIS
# ---------------------------
st.subheader("📌 Claim Status")

status_chart = px.pie(filtered_df, names="status", title="Claim Status Distribution")
st.plotly_chart(status_chart, use_container_width=True)

# ---------------------------
# TOP PROVIDERS
# ---------------------------
st.subheader("🏆 Top Providers")

top_providers = (
    filtered_df.groupby("name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(top_providers, x="name", y="quantity", title="Top Food Providers")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📋 Data Table")

st.dataframe(filtered_df)

# ---------------------------
# CONTACT INFO
# ---------------------------
st.subheader("📞 Provider Contacts")

contacts = filtered_df[["name", "city", "contact"]].drop_duplicates()
st.dataframe(contacts)