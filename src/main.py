import os
import time
from threading import Thread
import logging
import shutil
import datetime
import schedule

from init_cust_logging import initlogging

initlogging() # Call initlogging() ASAP when starting the container

logging.info("Starting...")

if os.path.exists('./cache'):
    logging.debug("Cache folder exists! Cleaning up...")
    shutil.rmtree('./cache')


logging.info("Welcome! Preparing for first run...")

now = datetime.datetime.now()
now_human = now.strftime("%Y-%m-%d %H:%M:%S")
now_unix = time.time()

# Looking for backup time ENV, Will default to 00:00 if not set (midnight)
backup_time = os.getenv('BACKUP_TIME', '00:00')
logging.info(f"Backup time set to {backup_time} (We will still run a backup now)")
logging.info("My timezone is currently: " + time.tzname[0])
logging.info(f"Current time is: {now_human} ({now_unix})")


def backup():
    logging.debug("Running backup...")
    # Hand off to backup script here
    pass

def run_threaded(job_func):
    logging.debug("Running job in a new thread. | Job: " + str(job_func))
    job_thread = Thread(target=job_func)
    job_thread.start()

# Run Backup now
logging.debug("Calling backup() now")
run_threaded(backup)

# Schedule should never run in the non-primary thread
logging.debug("Setting up schedule for daily backup...")
schedule.every().day.at(backup_time).do(run_threaded, backup)

logging.info("Setup complete! Handing off to schedule...")
while 1:
    schedule.run_pending()
    time.sleep(1)