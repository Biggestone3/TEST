import azure.functions as func
import datetime
import json
import logging
from lna_crawlers import crawler
app = func.FunctionApp()

app.add_extension('TimerBinding')

@app.timer_trigger(schedule="0 */3 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def MyTimerFunction(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    crawler.run()
    logging.info('Python timer trigger function executed.')