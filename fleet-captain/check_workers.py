import time
import datetime
import pytz
from config_model import worker_config
from cluster import cluster
from report import  report
from email_handler import  email_handler
import logging

logging.basicConfig(
    level=logging.INFO, filename='logs/fleet.log'
)
def run():
    logger = logging.getLogger(__name__)
    current_time = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d %H:%M')
    logging.info("\n**************")
    logging.info("Time:{} | Version:{}".format(current_time, "V2.0 Enabled Deletion"))
    messages = []
    alarm = 0
    terminating = 0
    time.time()
    for x in range(0,10):
        running_time = datetime.datetime.now(tz=pytz.timezone('Australia/Sydney')).strftime('%Y-%m-%d %H:%M')
        now = time.time() -36000
        record = worker_config.get_record(str(x))
        if record is not 0:
            last_update_time_diff = int(now) - record.lastUpdateTime
            last_index = record.lastIndex
            r_object = report(x, last_update_time_diff, last_index, record.isActive, True)
            if record.isActive:
                if(last_update_time_diff>150):
                    r_object.is_healthy = False
                    alarm = 1
                    if(last_update_time_diff>300):
                        terminating =1
                        r_object.terminating = True
                        logger.info("Terminating work:{}".format(x))
                        ports = cluster.delete_tasks(str(x))
                        r_object.port = ports
            logging.info("{}\t{}\t{}\t{}\t{}\t{}".format(x, last_update_time_diff, last_index,r_object.is_active, r_object.is_healthy, r_object.terminating))
            messages.append(r_object)

    # if(alarm==1):
    email_handler.process_item(messages, running_time, alarm, terminating)


run()
