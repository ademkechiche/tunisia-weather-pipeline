import pandas as pd

from src.transformation import (
    aggregate_region_temperatures,
    build_current_weather_df,
    build_daily_forecast_df,
    classify_alert,
    classify_comfort_level,
    enrich_with_city_metadata,
)


def sample_payloads():
    return [
        {
            "city": "Tunis",
            "current": {
                "time": "2026-04-22T12:00",
                "temperature_2m": 24.0,
                "relative_humidity_2m": 55,
                "wind_speed_10m": 18.0,
                "weather_code": 1,
            },
            "daily": {
                "time": ["2026-04-22", "2026-04-23"],
                "temperature_2m_max": [28.0, 30.0],
                "temperature_2m_min": [18.0, 20.0],
                "precipitation_sum": [0.0, 2.5],
            },
        },
        {
            "city": "Sfax",
            "current": {
                "time": "2026-04-22T12:00",
                "temperature_2m": 33.0,
                "relative_humidity_2m": 40,
                "wind_speed_10m": 22.0,
                "weather_code": 2,
            },
            "daily": {
                "time": ["2026-04-22", "2026-04-23"],
                "temperature_2m_max": [36.0, 39.0],
                "temperature_2m_min": [24.0, 25.0],
                "precipitation_sum": [0.0, 12.0],
            },
        },
    ]


def cities_df():
    return pd.DataFrame({"city": ["Tunis", "Sfax"], "region": ["Tunis", "Sfax"]})


def test_classify_comfort_level():
    assert classify_comfort_level(8) == "Cold"
    assert classify_comfort_level(24) == "Comfortable"
    assert classify_comfort_level(37) == "Extreme Heat"


def test_classify_alert():
    assert classify_alert(39, 10, 0) == "High"
    assert classify_alert(33, 10, 0) == "Medium"
    assert classify_alert(24, 10, 0) == "Low"


def test_build_current_weather_df():
    df = build_current_weather_df(sample_payloads())
    assert len(df) == 2
    assert "comfort_level" in df.columns
    assert df.loc[df["city"] == "Tunis", "temperature_c"].iloc[0] == 24.0


def test_build_daily_forecast_df():
    df = build_daily_forecast_df(sample_payloads())
    assert len(df) == 4
    assert "temp_avg_c" in df.columns
    assert df["alert_level"].isin(["Low", "Medium", "High"]).all()


def test_enrichment_and_region_aggregation():
    current_df = build_current_weather_df(sample_payloads())
    enriched = enrich_with_city_metadata(current_df, cities_df())
    assert "region" in enriched.columns
    region_summary = aggregate_region_temperatures(enriched)
    assert len(region_summary) == 2
    assert set(region_summary.columns) == {"region", "avg_temperature_c", "avg_wind_speed_kmh"}
