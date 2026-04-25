from __future__ import annotations

import pandas as pd


def classify_comfort_level(temp_c: float) -> str:
    if temp_c < 10:
        return "Cold"
    if temp_c < 20:
        return "Cool"
    if temp_c <= 28:
        return "Comfortable"
    if temp_c <= 35:
        return "Hot"
    return "Extreme Heat"


def classify_alert(temp_c: float, wind_speed: float, precipitation_sum: float) -> str:
    if temp_c >= 38 or wind_speed >= 45:
        return "High"
    if temp_c >= 32 or precipitation_sum >= 10:
        return "Medium"
    return "Low"


def build_current_weather_df(payloads: list[dict]) -> pd.DataFrame:
    rows = []
    for payload in payloads:
        current = payload["current"]
        rows.append(
            {
                "city": payload["city"],
                "timestamp": pd.to_datetime(current["time"]),
                "temperature_c": current["temperature_2m"],
                "humidity_pct": current["relative_humidity_2m"],
                "wind_speed_kmh": current["wind_speed_10m"],
                "weather_code": current["weather_code"],
            }
        )
    df = pd.DataFrame(rows)
    df["comfort_level"] = df["temperature_c"].apply(classify_comfort_level)
    df["snapshot_date"] = df["timestamp"].dt.date.astype(str)
    return df


def build_daily_forecast_df(payloads: list[dict]) -> pd.DataFrame:
    rows = []
    for payload in payloads:
        daily = payload["daily"]
        for i, date_val in enumerate(daily["time"]):
            tmax = daily["temperature_2m_max"][i]
            tmin = daily["temperature_2m_min"][i]
            precip = daily["precipitation_sum"][i]
            rows.append(
                {
                    "city": payload["city"],
                    "date": pd.to_datetime(date_val).date().isoformat(),
                    "temp_max_c": tmax,
                    "temp_min_c": tmin,
                    "temp_avg_c": round((tmax + tmin) / 2, 2),
                    "precipitation_mm": precip,
                    "alert_level": classify_alert((tmax + tmin) / 2, 0, precip),
                }
            )
    return pd.DataFrame(rows)


def enrich_with_city_metadata(df: pd.DataFrame, cities_df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.merge(cities_df[["city", "region"]], on="city", how="left")
    return enriched


def aggregate_region_temperatures(current_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        current_df.groupby("region", as_index=False)
        .agg(avg_temperature_c=("temperature_c", "mean"), avg_wind_speed_kmh=("wind_speed_kmh", "mean"))
        .round(2)
    )
    return grouped
