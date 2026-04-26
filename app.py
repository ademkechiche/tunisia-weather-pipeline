import datetime
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.config import DB_PATH
from src.storage import read_table

st.set_page_config(page_title="Tunisia Weather Pipeline", layout="wide")
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #eef5ff 100%);
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #1f2937;
}

h2, h3 {
    color: #1f2937;
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #0f172a;
    font-size: 2rem;
}

[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.stAlert {
    border-radius: 16px;
}

section[data-testid="stSidebar"] {
    background: #eef4fb;
    border-right: 1px solid #dbeafe;
}

hr {
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
    margin-bottom: 18px;
}

.small-muted {
    color: #64748b;
    font-size: 0.95rem;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 22px;
    margin: 34px 0 28px 0;
}

.kpi-card {
    padding: 26px;
    border-radius: 24px;
    color: white;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
    min-height: 145px;
}

.kpi-card.blue {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
}

.kpi-card.cyan {
    background: linear-gradient(135deg, #0891b2, #0e7490);
}

.kpi-card.orange {
    background: linear-gradient(135deg, #f97316, #ea580c);
}

.kpi-card.dark {
    background: linear-gradient(135deg, #0f172a, #334155);
}

.kpi-label {
    font-size: 0.95rem;
    opacity: 0.88;
    margin-bottom: 14px;
}

.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
}

.kpi-value.small {
    font-size: 1.7rem;
}

.kpi-sub {
    margin-top: 14px;
    font-size: 0.85rem;
    opacity: 0.82;
}
</style>
""", unsafe_allow_html=True)


refresh_count = st_autorefresh(interval=10000, key="dashboard_autorefresh")

st.markdown("""
# Tunisia Weather Monitoring Dashboard
<div class="small-muted">
End-to-end data engineering project: ingestion, storage, transformation, orchestration, and visualization.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

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
latest_df = latest_df.drop_duplicates(subset=["city"], keep="last")
cities = sorted(latest_df["city"].unique())
selected_city = st.sidebar.selectbox("Select a city", cities)

st.sidebar.info("Dashboard auto-refreshes every 10 seconds.")
st.sidebar.caption(f"Latest API weather time: {latest_ts}")

selected_city_df = latest_df[latest_df["city"] == selected_city]
selected_forecast = daily_df[daily_df["city"] == selected_city].copy()

avg_temp = round(latest_df["temperature_c"].mean(), 2)
hottest_city = latest_df.sort_values("temperature_c", ascending=False).iloc[0]["city"]
latest_time_short = str(latest_ts)[:16]

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card blue">
        <div class="kpi-label">Cities monitored</div>
        <div class="kpi-value">{len(cities)}</div>
        <div class="kpi-sub">Active Tunisian locations</div>
    </div>
    <div class="kpi-card cyan">
        <div class="kpi-label">Average temperature</div>
        <div class="kpi-value">{avg_temp}°C</div>
        <div class="kpi-sub">Latest city snapshot</div>
    </div>
    <div class="kpi-card orange">
        <div class="kpi-label">Hottest city now</div>
        <div class="kpi-value">{hottest_city}</div>
        <div class="kpi-sub">Highest current temperature</div>
    </div>
    <div class="kpi-card dark">
        <div class="kpi-label">Latest API update</div>
        <div class="kpi-value small">{latest_time_short}</div>
        <div class="kpi-sub">Observation timestamp</div>
    </div>
</div>
""", unsafe_allow_html=True)
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