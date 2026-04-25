import datetime
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.config import DB_PATH
from src.storage import read_table

st.set_page_config(page_title="Tunisia Weather Pipeline", layout="wide")

refresh_count = st_autorefresh(interval=10000, key="dashboard_autorefresh")

st.title("Tunisia Weather Monitoring Dashboard")
st.caption(
    "End-to-end data engineering project: ingestion, storage, transformation, "
    "orchestration, and visualization."
)

if not DB_PATH.exists():
    st.warning("Database not found yet. Run `python run_pipeline.py` first.")
    st.stop()

current_df = read_table("SELECT * FROM current_weather")
daily_df = read_table("SELECT * FROM daily_forecast")
region_df = read_table("SELECT * FROM region_summary")

if current_df.empty:
    st.warning("No data available yet. Run the pipeline first.")
    st.stop()

if "timestamp" not in current_df.columns:
    st.error("Missing timestamp column in current_weather table.")
    st.stop()

latest_ts = pd.to_datetime(current_df["timestamp"]).max()
latest_df = current_df[pd.to_datetime(current_df["timestamp"]) == latest_ts].copy()

cities = sorted(latest_df["city"].unique())
selected_city = st.sidebar.selectbox("Select a city", cities)

st.sidebar.info("Dashboard auto-refreshes every 10 seconds.")
st.sidebar.caption(f"Latest API weather time: {latest_ts}")

selected_city_df = latest_df[latest_df["city"] == selected_city]
selected_forecast = daily_df[daily_df["city"] == selected_city].copy()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Cities monitored", len(cities))
col2.metric("Latest average temp (°C)", round(latest_df["temperature_c"].mean(), 2))
col3.metric(
    "Hottest city now",
    latest_df.sort_values("temperature_c", ascending=False).iloc[0]["city"],
)
col4.metric("Latest API weather time", str(latest_ts))

st.caption(
    "Note: the dashboard refreshes frequently, but the external weather API may only "
    "publish new observations every 10–15 minutes."
)

st.subheader(f"Current conditions — {selected_city}")
st.dataframe(
    selected_city_df[
        [
            "city",
            "region",
            "temperature_c",
            "humidity_pct",
            "wind_speed_kmh",
            "comfort_level",
        ]
    ],
    use_container_width=True,
)

left, right = st.columns(2)

with left:
    st.subheader("Forecast temperatures")
    if not selected_forecast.empty:
        chart_df = selected_forecast[
            ["date", "temp_min_c", "temp_avg_c", "temp_max_c"]
        ].set_index("date")
        st.line_chart(chart_df)
    else:
        st.info("No forecast data available for this city.")

with right:
    st.subheader("Forecast precipitation")
    if not selected_forecast.empty:
        rain_df = selected_forecast[["date", "precipitation_mm"]].set_index("date")
        st.bar_chart(rain_df)
    else:
        st.info("No precipitation forecast available for this city.")

st.subheader("Regional summary")
st.dataframe(region_df, use_container_width=True)

st.subheader("Latest snapshot across cities")
st.dataframe(
    latest_df[
        [
            "city",
            "region",
            "temperature_c",
            "humidity_pct",
            "wind_speed_kmh",
            "comfort_level",
        ]
    ].sort_values("temperature_c", ascending=False),
    use_container_width=True,
)

alert_df = daily_df[
    ["city", "date", "alert_level", "precipitation_mm", "temp_avg_c"]
].copy()

st.subheader("Forecast alert monitoring")
st.dataframe(
    alert_df.sort_values(["alert_level", "date"], ascending=[False, True]),
    use_container_width=True,
)

# ---------------- HIDDEN DEBUG PANEL - SEPARATE BOTTOM SECTION ----------------
st.divider()

with st.expander("🛠 Debug Panel", expanded=False):
    st.markdown("### Debug Info")

    st.write("Dashboard refresh count:", refresh_count)
    st.write("Dashboard current time:", datetime.datetime.now().strftime("%H:%M:%S"))
    st.write("Rows in current_weather:", len(current_df))
    st.write("Database file:", str(DB_PATH.name))

    latest_api_time = pd.to_datetime(current_df["timestamp"]).max()
    st.write("Latest API weather time:", latest_api_time)

    if "ingested_at" in current_df.columns:
        latest_ingestion_time = pd.to_datetime(current_df["ingested_at"]).max()
        st.write("Latest pipeline ingestion:", latest_ingestion_time)
    else:
        st.info("No ingested_at column found. API timestamp is used instead.")

    selected_debug_city = st.selectbox(
        "Debug city",
        sorted(current_df["city"].unique()),
        key="debug_city",
    )

    debug_city_df = current_df[current_df["city"] == selected_debug_city].copy()
    debug_city_df["timestamp"] = pd.to_datetime(debug_city_df["timestamp"])

    latest_row = debug_city_df.sort_values("timestamp", ascending=False).iloc[0]

    st.write(
        f"{selected_debug_city}: {latest_row['temperature_c']}°C "
        f"(refresh #{refresh_count})"
    )
# ---------------------------------------------------------------------------