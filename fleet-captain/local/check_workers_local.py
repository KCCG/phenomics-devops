import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import datetime
import pytz
import logging
from  config_model import worker_config
from report import  report

logging.basicConfig(
    level=logging.INFO, filename='logs/fleet.log'
)
def run():
    logger = logging.getLogger(__name__)
    messages = []
    alarm = 0
    terminating = 0
    time.time()

    print("WorkerID\tLastRun\tPMIDs\tActive\tHealthy\tTerminating")
    for x in range(0,10):
        running_time = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d %H:%M')
        now = time.time() -36000
        record = worker_config.get_record(str(x))
        if record is not 0:
            last_update_time_diff = int(now) - record.lastUpdateTime
            last_index = record.lastIndex
            r_object = report(x, last_update_time_diff, last_index, record.isActive, True)
            if record.isActive:
                if(last_update_time_diff>125):
                    r_object.is_healthy = False
                    alarm = 1
                    if(last_update_time_diff>300):
                        terminating =1
                        r_object.terminating = True
                        logger.info("Terminating work:{}".format(x))
                        port = ""
                        r_object.port = port
            print("{}\t{}\t{}\t{}\t{}\t{}".format(x, last_update_time_diff, last_index,r_object.is_active, r_object.is_healthy, r_object.terminating))

# if(alarm==1):
#     email_handler.process_item(messages, running_time, alarm, terminating)

run()
