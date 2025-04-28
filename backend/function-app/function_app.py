import importlib
import importlib.metadata
import logging
import os
import sys
from datetime import datetime, timedelta, timezone

import azure.functions as func
from aggregators.time_based_aggregator import TimeBasedAggregator
from dotenv import load_dotenv
from lna_db.db.mongo import init_database

app = func.FunctionApp()

is_local = os.environ.get("AZURE_FUNCTIONS_ENVIRONMENT") == "Development"


@app.timer_trigger(
    schedule="* */30 * * * *",
    arg_name="myTimer",
    run_on_startup=is_local,  # Only run on startup in local environment
    use_monitor=False,
)
async def story_aggregator_function(myTimer: func.TimerRequest) -> None:
    logging.info(f"Python path: {sys.path}")
    logging.info(f"Python interpreter: {sys.executable}")
    execution_start_time = datetime.now(timezone.utc)
    logging.info("Story Aggregator Function executed at %s", execution_start_time)
    version = importlib.metadata.version("lna_db")
    logging.info(f"lna_db version: {version}")
    load_dotenv()
    username = str(os.environ.get("username_of_db"))
    password = str(os.environ.get("password_of_db"))
    mongo_uri_part2 = str(os.environ.get("mongo_uri_part2"))

    logging.info("initializing database")
    await init_database(
        username=username,
        password=password,
        mongo_uri_part2=mongo_uri_part2,
    )

    logging.info("calling time based aggregator")
    time_based_aggregator = TimeBasedAggregator()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    await time_based_aggregator.aggregate_stories(
        start_time=start_time,
        end_time=end_time,
    )

    execution_end_time = datetime.now(timezone.utc)
    duration_ms = (execution_end_time - execution_start_time).total_seconds() * 1000
    logging.info(
        f"Story Aggregator Function done at {execution_end_time}."
        + f"duration: {duration_ms} ms"
    )
