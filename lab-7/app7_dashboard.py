import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Dashboard")

# Fake data (cached so it doesn't change on every filter click)
@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "Year": rng.choice([2022, 2023, 2024], 200),
        "Region": rng.choice(["North", "South", "East", "West"], 200),
        "Product": rng.choice(["A", "B", "C"], 200),
        "Sales": rng.integers(1000, 10000, 200),
    })

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
years = sorted(df["Year"].unique())
regions = sorted(df["Region"].unique())
products = sorted(df["Product"].unique())

year = st.sidebar.multiselect("Year", years, default=years)
region = st.sidebar.multiselect("Region", regions, default=regions)
product = st.sidebar.multiselect("Product", products, default=products)

filtered = df[
    df["Year"].isin(year)
    & df["Region"].isin(region)
    & df["Product"].isin(product)
]

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"{filtered['Sales'].sum():,}")
avg_sales = int(filtered["Sales"].mean()) if not filtered.empty else 0
c2.metric("Avg Sales", f"{avg_sales:,}")
c3.metric("Records", len(filtered))

# Charts
if filtered.empty:
    st.warning("No data for the selected filters.")
else:
    st.subheader("Sales by Region")
    st.bar_chart(filtered.groupby("Region")["Sales"].sum())

    st.subheader("Sales by Year")
    st.line_chart(filtered.groupby("Year")["Sales"].sum())