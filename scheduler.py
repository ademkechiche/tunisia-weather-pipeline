from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import BATCH_INTERVAL_HOURS, STREAM_INTERVAL_MINUTES
from src.logging_config import get_logger
from src.pipeline import run_pipeline

logger = get_logger(__name__)


def run_stream_like_job():
    logger.info("Running near real-time weather snapshot job")
    run_pipeline()


def run_batch_job():
    logger.info("Running scheduled batch refresh job")
    run_pipeline()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_stream_like_job, "interval", minutes=STREAM_INTERVAL_MINUTES, id="stream_like_job")
    scheduler.add_job(run_batch_job, "interval", hours=BATCH_INTERVAL_HOURS, id="batch_job")
    logger.info("Scheduler started")
    run_pipeline()
    scheduler.start()
