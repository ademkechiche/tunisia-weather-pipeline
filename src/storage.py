import sqlite3

import pandas as pd

from src.config import DB_PATH
from src.logging_config import get_logger

logger = get_logger(__name__)


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def write_table(df: pd.DataFrame, table_name: str, if_exists: str = "append") -> None:
    conn = get_connection()
    try:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
        logger.info(f"Wrote {len(df)} rows to {table_name}")
    finally:
        conn.close()


def read_table(query: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()
