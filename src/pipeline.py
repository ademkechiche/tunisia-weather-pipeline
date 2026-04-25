from src.ingestion import ingest_all_weather, load_city_metadata
from src.logging_config import get_logger
from src.storage import write_table
from src.transformation import (
    aggregate_region_temperatures,
    build_current_weather_df,
    build_daily_forecast_df,
    enrich_with_city_metadata,
)

logger = get_logger(__name__)


def run_pipeline() -> None:
    logger.info("Starting pipeline execution")
    payloads = ingest_all_weather()
    cities = load_city_metadata()

    current_df = build_current_weather_df(payloads)
    current_df = enrich_with_city_metadata(current_df, cities)

    daily_df = build_daily_forecast_df(payloads)
    daily_df = enrich_with_city_metadata(daily_df, cities)

    region_df = aggregate_region_temperatures(current_df)

    write_table(current_df, "current_weather", if_exists="append")
    write_table(daily_df, "daily_forecast", if_exists="replace")
    write_table(region_df, "region_summary", if_exists="replace")
    logger.info("Pipeline execution completed")
