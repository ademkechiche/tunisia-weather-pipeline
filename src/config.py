from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
DB_PATH = BASE_DIR / "weather_pipeline.db"
CITIES_CSV = DATA_DIR / "cities.csv"
LOG_LEVEL = "INFO"
REQUEST_TIMEOUT = 25
RETRY_COUNT = 3
STREAM_INTERVAL_MINUTES = 1
BATCH_INTERVAL_HOURS = 6
