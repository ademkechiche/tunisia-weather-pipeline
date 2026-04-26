"""
Tunisia Weather Monitoring Dashboard — v4 (Light Theme)
"""

import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from src.config import DB_PATH
from src.storage import read_table

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Tunisia Weather",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# LIGHT THEME CSS
# ─────────────────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, .stApp {
    background-color: #f5f7fa !important;
    font-family: 'Outfit', sans-serif !important;
    color: #1a1f2e !important;
}
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label { color: #1a1f2e !important; }

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    color: #1a1f2e !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #ffffff;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #e2e8f0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
    padding: 8px 20px;
    color: #64748b !important;
    font-weight: 500;
    font-size: 0.9rem;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}
[data-testid="stMetricLabel"] p {
    color: #64748b !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] { color: #1a1f2e !important; }

/* Headings & text */
h1 { font-size: 2.2rem !important; font-weight: 800 !important; color: #1a1f2e !important; letter-spacing: -0.02em !important; }
h2, h3 { color: #1a1f2e !important; font-weight: 700 !important; }
p { color: #1a1f2e; }

/* Divider */
hr { border-color: #e2e8f0 !important; margin: 1.5rem 0 !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
}

/* Alerts */
.stAlert { border-radius: 12px !important; }

/* Caption */
.stCaption p { color: #94a3b8 !important; font-size: 0.82rem !important; }

/* Plotly */
.js-plotly-plot { border-radius: 14px; overflow: hidden; }
</style>
""")

# ─────────────────────────────────────────────
# AUTO-REFRESH
# ─────────────────────────────────────────────
st_autorefresh(interval=30_000, key="dashboard_refresh")

# ─────────────────────────────────────────────
# PLOTLY LIGHT THEME
# ─────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#ffffff",
    font=dict(family="Outfit", color="#64748b", size=12),
    xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", tickcolor="#e2e8f0", color="#64748b"),
    yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", tickcolor="#e2e8f0", color="#64748b"),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#1a1f2e")),
)
COLORS = ["#2563eb", "#f97316", "#16a34a", "#ef4444", "#0891b2", "#7c3aed"]

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_data():
    current_df = read_table("SELECT * FROM current_weather")
    daily_df   = read_table("SELECT * FROM daily_forecast")
    region_df  = read_table("SELECT * FROM region_summary")
    return current_df, daily_df, region_df


if not DB_PATH.exists():
    st.warning("Database not found. Run `python run_pipeline.py` first.")
    st.stop()

current_df, daily_df, region_df = load_data()

if current_df.empty:
    st.warning("No data available yet. Run the pipeline first.")
    st.stop()

if "timestamp" not in current_df.columns:
    st.error("Missing `timestamp` column in current_weather table.")
    st.stop()

# ─────────────────────────────────────────────
# DERIVE LATEST SNAPSHOT
# ─────────────────────────────────────────────
current_df["timestamp"] = pd.to_datetime(current_df["timestamp"])
latest_ts = current_df["timestamp"].max()
latest_df = (
    current_df[current_df["timestamp"] == latest_ts]
    .drop_duplicates(subset=["city"], keep="last")
    .copy()
)
cities = sorted(latest_df["city"].unique())

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌤 TN Weather")
    st.caption("Monitoring Pipeline")
    st.markdown("---")

    selected_city = st.selectbox("Selected city", cities)

    row = latest_df[latest_df["city"] == selected_city].iloc[0]
    comfort = str(row.get("comfort_level", "—"))

    st.markdown("---")
    st.markdown(f"**{row['city']}** · {row['region']}")
    st.metric("Temperature", f"{row['temperature_c']:.1f} °C")
    m1, m2 = st.columns(2)
    m1.metric("Humidity",    f"{row['humidity_pct']:.0f}%")
    m2.metric("Wind",        f"{row['wind_speed_kmh']:.0f} km/h")
    st.info(f"Comfort: **{comfort}**")

    st.markdown("---")
    st.caption(f"Last update · {latest_ts.strftime('%d %b %Y %H:%M')}")
    st.caption("Auto-refreshes every 30 s")

    with st.expander("🛠 Debug", expanded=False):
        st.write("Rows loaded:", len(current_df))
        st.write("DB:", DB_PATH.name)
        st.write("Time:", datetime.datetime.now().strftime("%H:%M:%S"))
        if "ingested_at" in current_df.columns:
            st.write("Ingested:", pd.to_datetime(current_df["ingested_at"]).max())

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("# Tunisia Weather Dashboard")
st.caption("Real-time monitoring across Tunisian cities — ingestion · storage · transformation · visualization")
st.markdown("---")

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
avg_temp     = round(latest_df["temperature_c"].mean(), 1)
avg_humidity = round(latest_df["humidity_pct"].mean(), 1)
hottest_row  = latest_df.sort_values("temperature_c", ascending=False).iloc[0]
alert_count  = int((daily_df["alert_level"].str.lower() != "none").sum()) if "alert_level" in daily_df.columns else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🏙 Cities",        len(cities))
k2.metric("🌡 Avg Temp",      f"{avg_temp} °C")
k3.metric("🔥 Hottest",       hottest_row["city"], f"{hottest_row['temperature_c']:.1f} °C")
k4.metric("💧 Avg Humidity",  f"{avg_humidity}%")
k5.metric("⚠️ Active Alerts", alert_count)

st.markdown("---")

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab_overview, tab_forecast, tab_alerts, tab_regions = st.tabs([
    "📍 Current Conditions",
    "📈 Forecast",
    "⚠️ Alerts",
    "🗺 Regions",
])

# ── TAB 1 ────────────────────────────────────
with tab_overview:
    left_col, right_col = st.columns([3, 2], gap="large")

    with left_col:
        st.subheader("All cities — latest snapshot")
        display_cols = {
            "city": "City", "region": "Region",
            "temperature_c": "Temp (°C)", "humidity_pct": "Humidity (%)",
            "wind_speed_kmh": "Wind (km/h)", "comfort_level": "Comfort",
        }
        overview_df = latest_df[list(display_cols.keys())].rename(columns=display_cols).reset_index(drop=True)
        st.dataframe(
            overview_df,
            use_container_width=True,
            column_config={
                "Temp (°C)":    st.column_config.NumberColumn(format="%.1f °C"),
                "Humidity (%)": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.0f%%"),
                "Wind (km/h)":  st.column_config.NumberColumn(format="%.0f km/h"),
            },
            hide_index=True,
        )

    with right_col:
        st.subheader("Temperature distribution")
        sorted_df = latest_df.sort_values("temperature_c", ascending=True)
        fig_bar = px.bar(
            sorted_df, x="temperature_c", y="city", orientation="h",
            color="temperature_c",
            color_continuous_scale=["#93c5fd", "#f97316", "#ef4444"],
            labels={"temperature_c": "°C", "city": ""},
        )
        fig_bar.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=360)
        fig_bar.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("Humidity vs Temperature")
    fig_scatter = px.scatter(
        latest_df, x="temperature_c", y="humidity_pct", text="city",
        color="wind_speed_kmh",
        color_continuous_scale=["#2563eb", "#7c3aed"],
        size=[14] * len(latest_df),
        labels={"temperature_c": "Temperature (°C)", "humidity_pct": "Humidity (%)", "wind_speed_kmh": "Wind (km/h)"},
    )
    fig_scatter.update_traces(textposition="top center", textfont=dict(color="#1a1f2e", size=11))
    fig_scatter.update_layout(**PLOTLY_LAYOUT, height=320, coloraxis_colorbar=dict(title="Wind km/h"))
    st.plotly_chart(fig_scatter, use_container_width=True)


# ── TAB 2 ────────────────────────────────────
with tab_forecast:
    selected_forecast = daily_df[daily_df["city"] == selected_city].copy()

    if selected_forecast.empty:
        st.info(f"No forecast data available for {selected_city}.")
    else:
        st.subheader(f"7-day forecast — {selected_city}")
        fc_left, fc_right = st.columns(2, gap="large")

        with fc_left:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=selected_forecast["date"], y=selected_forecast["temp_max_c"],
                name="Max", line=dict(color="#ef4444", width=2), fill=None,
            ))
            fig_temp.add_trace(go.Scatter(
                x=selected_forecast["date"], y=selected_forecast["temp_avg_c"],
                name="Avg", line=dict(color="#f97316", width=2, dash="dot"),
                fill="tonexty", fillcolor="rgba(239,68,68,0.07)",
            ))
            fig_temp.add_trace(go.Scatter(
                x=selected_forecast["date"], y=selected_forecast["temp_min_c"],
                name="Min", line=dict(color="#2563eb", width=2),
                fill="tonexty", fillcolor="rgba(37,99,235,0.07)",
            ))
            fig_temp.update_layout(**PLOTLY_LAYOUT, title="Temperature band (°C)", height=320)
            st.plotly_chart(fig_temp, use_container_width=True)

        with fc_right:
            fig_rain = px.bar(
                selected_forecast, x="date", y="precipitation_mm",
                color="precipitation_mm",
                color_continuous_scale=["#bfdbfe", "#2563eb", "#1e40af"],
                labels={"precipitation_mm": "mm", "date": ""},
            )
            fig_rain.update_layout(**PLOTLY_LAYOUT, title="Precipitation (mm)", height=320, coloraxis_showscale=False)
            fig_rain.update_traces(marker_line_width=0)
            st.plotly_chart(fig_rain, use_container_width=True)

        st.subheader("Forecast table")
        fc_display = selected_forecast[["date", "temp_min_c", "temp_avg_c", "temp_max_c", "precipitation_mm"]].copy()
        fc_display.columns = ["Date", "Min (°C)", "Avg (°C)", "Max (°C)", "Precip (mm)"]
        st.dataframe(
            fc_display.reset_index(drop=True),
            use_container_width=True,
            column_config={
                "Min (°C)":    st.column_config.NumberColumn(format="%.1f °C"),
                "Avg (°C)":    st.column_config.NumberColumn(format="%.1f °C"),
                "Max (°C)":    st.column_config.NumberColumn(format="%.1f °C"),
                "Precip (mm)": st.column_config.NumberColumn(format="%.1f mm"),
            },
            hide_index=True,
        )


# ── TAB 3 ────────────────────────────────────
with tab_alerts:
    if "alert_level" not in daily_df.columns:
        st.info("No alert_level column found in forecast data.")
    else:
        alert_df = daily_df[["city", "date", "alert_level", "precipitation_mm", "temp_avg_c"]].copy()

        high_alerts = int((alert_df["alert_level"].str.lower() == "high").sum())
        med_alerts  = int((alert_df["alert_level"].str.lower() == "medium").sum())
        low_alerts  = int((alert_df["alert_level"].str.lower() == "low").sum())

        a1, a2, a3 = st.columns(3)
        a1.metric("🔴 High",   high_alerts)
        a2.metric("🟡 Medium", med_alerts)
        a3.metric("🟢 Low",    low_alerts)

        st.markdown("")
        high_df = alert_df[alert_df["alert_level"].str.lower() == "high"]
        if not high_df.empty:
            for _, ar in high_df.iterrows():
                st.warning(
                    f"⚠️ **{ar['city']}** — {ar['date']}  |  "
                    f"Avg {ar['temp_avg_c']:.1f}°C · {ar['precipitation_mm']:.1f} mm rain"
                )

        st.subheader("All forecast alerts")
        sorted_alerts = alert_df.sort_values(["alert_level", "date"], ascending=[False, True]).reset_index(drop=True)
        sorted_alerts.columns = ["City", "Date", "Alert Level", "Precip (mm)", "Avg Temp (°C)"]
        st.dataframe(
            sorted_alerts,
            use_container_width=True,
            column_config={
                "Precip (mm)":   st.column_config.NumberColumn(format="%.1f mm"),
                "Avg Temp (°C)": st.column_config.NumberColumn(format="%.1f °C"),
            },
            hide_index=True,
        )


# ── TAB 4 ────────────────────────────────────
with tab_regions:
    st.subheader("Regional summary")
    if region_df.empty:
        st.info("No regional data available.")
    else:
        num_cols = region_df.select_dtypes("number").columns.tolist()
        if num_cols and "region" in region_df.columns:
            fig_reg = px.bar(
                region_df, x="region", y=num_cols[0],
                color="region", color_discrete_sequence=COLORS,
                labels={"region": "Region", num_cols[0]: num_cols[0].replace("_", " ").title()},
            )
            fig_reg.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False)
            st.plotly_chart(fig_reg, use_container_width=True)

        st.dataframe(region_df.reset_index(drop=True), use_container_width=True, hide_index=True)
