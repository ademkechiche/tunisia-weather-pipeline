import pandas as pd
import streamlit as st

from src.config import DB_PATH
from src.storage import read_table

st.set_page_config(page_title="Tunisia Weather Pipeline", layout="wide")
st.title("Tunisia Weather Monitoring Dashboard")
st.caption("End-to-end data engineering project: ingestion, storage, transformation, orchestration, and visualization.")

if not DB_PATH.exists():
    st.warning("Database not found yet. Run `python run_pipeline.py` first.")
    st.stop()

current_df = read_table("SELECT * FROM current_weather")
daily_df = read_table("SELECT * FROM daily_forecast")
region_df = read_table("SELECT * FROM region_summary")

if current_df.empty:
    st.warning("No data available yet. Run the pipeline first.")
    st.stop()

latest_ts = pd.to_datetime(current_df["timestamp"]).max()
latest_df = current_df[pd.to_datetime(current_df["timestamp"]) == latest_ts].copy()

cities = sorted(latest_df["city"].unique())
selected_city = st.sidebar.selectbox("Select a city", cities)
selected_city_df = latest_df[latest_df["city"] == selected_city]
selected_forecast = daily_df[daily_df["city"] == selected_city].copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Cities monitored", len(cities))
col2.metric("Latest average temp (°C)", round(latest_df["temperature_c"].mean(), 2))
col3.metric("Hottest city now", latest_df.sort_values("temperature_c", ascending=False).iloc[0]["city"])
col4.metric("Last update", str(latest_ts))

st.subheader(f"Current conditions — {selected_city}")
st.dataframe(selected_city_df[["city", "region", "temperature_c", "humidity_pct", "wind_speed_kmh", "comfort_level"]], use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Forecast temperatures")
    if not selected_forecast.empty:
        chart_df = selected_forecast[["date", "temp_min_c", "temp_avg_c", "temp_max_c"]].set_index("date")
        st.line_chart(chart_df)
with right:
    st.subheader("Forecast precipitation")
    if not selected_forecast.empty:
        rain_df = selected_forecast[["date", "precipitation_mm"]].set_index("date")
        st.bar_chart(rain_df)

st.subheader("Regional summary")
st.dataframe(region_df, use_container_width=True)

st.subheader("Latest snapshot across cities")
st.dataframe(
    latest_df[["city", "region", "temperature_c", "humidity_pct", "wind_speed_kmh", "comfort_level"]]
    .sort_values("temperature_c", ascending=False),
    use_container_width=True,
)

alert_df = daily_df[["city", "date", "alert_level", "precipitation_mm", "temp_avg_c"]].copy()
st.subheader("Forecast alert monitoring")
st.dataframe(alert_df.sort_values(["alert_level", "date"], ascending=[False, True]), use_container_width=True)
