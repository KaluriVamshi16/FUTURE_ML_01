import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt   # ✅ FIXED

# -----------------------------
# PAGE CONFIG (FIRST STREAMLIT COMMAND)
# -----------------------------
st.set_page_config(
    page_title="Sales Forecast Dashboard",
    layout="wide"
)

# -----------------------------
# SAFE PATH (INDUSTRY STANDARD)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(BASE_DIR, "data", "superstore.csv")
forecast_path = os.path.join(BASE_DIR, "data", "future_sales_forecast.csv")

# -----------------------------
# LOAD DATA (ONLY ONCE ✅)
# -----------------------------
historical = pd.read_csv(data_path, encoding="latin-1")
forecast = pd.read_csv(forecast_path)

historical['Order Date'] = pd.to_datetime(historical['Order Date'])

monthly_sales = historical.resample('M', on='Order Date')['Sales'].sum().reset_index()

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Sales Demand Forecasting Dashboard")
st.write("Predicting future sales using Machine Learning for smarter business decisions.")

st.divider()

# -----------------------------
# KPI METRICS
# -----------------------------
total_sales = int(monthly_sales['Sales'].sum())
avg_sales = int(monthly_sales['Sales'].mean())
next_month_prediction = int(forecast['Forecasted Sales'].iloc[0])

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Historical Sales", f"${total_sales:,}")
col2.metric("📉 Average Monthly Sales", f"${avg_sales:,}")
col3.metric("🔮 Next Month Forecast", f"${next_month_prediction:,}")

st.divider()

# -----------------------------
# FORECAST CHART
# -----------------------------
st.subheader("📈 Sales Forecast vs Historical Trend")

fig, ax = plt.subplots(figsize=(14,6))

ax.plot(monthly_sales['Order Date'],
        monthly_sales['Sales'],
        label="Historical Sales")

ax.plot(pd.to_datetime(forecast['Order Date']),
        forecast['Forecasted Sales'],
        linestyle="dashed",
        label="Forecasted Sales")

ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Sales")

st.pyplot(fig)

st.divider()

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------
st.subheader("📌 Business Insights")

growth_rate = ((forecast['Forecasted Sales'].mean() - avg_sales) / avg_sales) * 100

if growth_rate > 0:
    insight = "Sales are expected to grow. Consider increasing inventory and staffing."
else:
    insight = "Sales may decline. Focus on promotions and cost optimization."

st.write(f"""
✅ The business generated **${total_sales:,}** in historical sales.

✅ Average monthly sales are approximately **${avg_sales:,}**.

✅ Forecast indicates a **{growth_rate:.2f}% change** in upcoming months.

👉 **Recommendation:** {insight}
""")

st.divider()

# -----------------------------
# RAW DATA
# -----------------------------
with st.expander("View Forecast Data"):
    st.dataframe(forecast)
