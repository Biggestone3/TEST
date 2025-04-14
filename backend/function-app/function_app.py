import datetime
import logging
import os
import sys

import azure.functions as func
from aggregators.time_based_aggregator import time_based_aggregator

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
    logging.info("Story Aggregator Function executed at %s", datetime.datetime.now())
    await time_based_aggregator()
