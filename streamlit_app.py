import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
   page_title="🛒 Superstore Business Performance Dashboard",
   page_icon="📊",
   layout="wide",
   initial_sidebar_state="expanded",
)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    url = "https://github.com/sna-ds/gdp-dashboard-hands-on/raw/5481eb4f5760d9620869710269306922a811670c/superstore_dataset.xlsx"
    df = pd.read_excel(url)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.to_period("M")
    return df

df = load_data()

# --- APP TITLE AND DESCRIPTION ---
st.title("🛒 Superstore Business Performance Dashboard")
st.markdown("""
**Superstore is a U.S.-based retail company seeking growth opportunities through a deeper understanding of its sales performance.**
This interactive application enables users to track sales and profit trends, identify key markets, and analyze both top-performing and underperforming products.

It helps business leaders answer key questions such as:
- Which cities and products contribute the most to sales and profit?
- How do sales trends evolve over time?
- Which categories or sub-categories are driving profit or causing losses?

With built-in filters, the app supports deeper exploration of regions, categories, and time periods to uncover actionable business insights.
""")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filters")

years = st.sidebar.multiselect("Select Year(s)", options=sorted(df["year"].unique()), default=sorted(df["year"].unique()))
regions = st.sidebar.multiselect("Select Region(s)", options=df["region"].unique(), default=df["region"].unique())
categories = st.sidebar.multiselect("Select Category", options=df["category"].unique(), default=df["category"].unique())
segments = st.sidebar.multiselect("Select Segment", options=df["segment"].unique(), default=df["segment"].unique())

# Filter dataframe
df_selection = df.query("year in @years and region in @regions and category in @categories and segment in @segments")

if df_selection.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- KEY METRICS ---
st.subheader("📊 Key Metrics")

total_customers = df_selection["customer_id"].nunique()
total_units = df_selection["quantity"].sum()
total_sales = df_selection["sales"].sum()
total_profit = df_selection["profit"].sum()

# Sales YoY Growth
sales_by_year = df_selection.groupby("year")["sales"].sum().sort_index()
sales_yoy = None
if len(sales_by_year) > 1:
    sales_yoy = ((sales_by_year.iloc[-1] - sales_by_year.iloc[-2]) / sales_by_year.iloc[-2]) * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", total_customers)
col2.metric("Total Units Sold", total_units)
col3.metric("Total Sales", f"${total_sales:,.0f}")
col4.metric("Sales YoY", f"{sales_yoy:.1f}%" if sales_yoy is not None else "N/A")
col5.metric("Total Profit", f"${total_profit:,.0f}")

st.markdown("---")

# --- SALES OVER TIME ---
st.subheader("📈 Sales Over Time")
sales_over_time = df_selection.groupby("month")["sales"].sum().reset_index()
sales_over_time["month"] = sales_over_time["month"].astype(str)
st.line_chart(sales_over_time.set_index("month"))

st.markdown("---")

# --- TOP PRODUCT & CITY ANALYSIS ---
st.subheader("🏙️ Top Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 Cities by Sales & Profit**")
    top_cities = df_selection.groupby("city")[["sales", "profit"]].sum().nlargest(10, "sales")
    st.bar_chart(top_cities)

with col2:
    st.markdown("**Top Categories by Sales & Profit**")
    top_cat = df_selection.groupby("category")[["sales", "profit"]].sum()
    st.bar_chart(top_cat)

st.markdown("**Top 10 Sub-Categories by Sales**")
top_subcat = df_selection.groupby("subcategory")[["sales", "profit"]].sum().nlargest(10, "sales")
st.bar_chart(top_subcat)

st.markdown("---")

# --- SALES VS PROFIT ---
st.subheader("💰 Sales vs Profit by Sub-Category")

sales_profit = df_selection.groupby("subcategory")[["sales", "profit"]].sum().sort_values("sales", ascending=False)
st.bar_chart(sales_profit)

st.markdown("---")

# --- RAW DATA ---
with st.expander("🔍 View Raw Data"):
    st.dataframe(df_selection)
    st.markdown(f"**Data Dimensions:** {df_selection.shape[0]} rows × {df_selection.shape[1]} columns")

st.write("Data Source: Superstore Dataset (Sample Business Data)")
