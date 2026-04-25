import json
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

from src.config import CITIES_CSV, RAW_DIR, REQUEST_TIMEOUT, RETRY_COUNT
from src.logging_config import get_logger

logger = get_logger(__name__)


def load_city_metadata() -> pd.DataFrame:
    return pd.read_csv(CITIES_CSV)


def fetch_weather_for_city(city: str, latitude: float, longitude: float) -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=auto&forecast_days=3"
    )

    last_error = None
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            logger.info(f"Fetching weather for {city}, attempt {attempt}")
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            payload = response.json()
            payload["city"] = city
            return payload
        except Exception as exc:  # pragma: no cover
            last_error = exc
            logger.error(f"Error while fetching weather for {city}: {exc}")
            time.sleep(min(attempt, 3))

    raise RuntimeError(f"Failed to fetch weather for {city}") from last_error


def save_raw_payload(city: str, payload: dict) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = RAW_DIR / f"{city.lower()}_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def ingest_all_weather() -> list[dict]:
    cities = load_city_metadata()
    payloads = []
    for row in cities.itertuples(index=False):
        payload = fetch_weather_for_city(row.city, row.latitude, row.longitude)
        save_raw_payload(row.city, payload)
        payloads.append(payload)
    return payloads
