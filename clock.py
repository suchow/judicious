from datetime import datetime, timedelta
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from pq import PQ
from psycopg2 import connect

from app import db, Task
import recruiters

# Set up connection to queue.
DB_URL_DEFAULT = 'postgresql://postgres@localhost/judicious'
DB_URL = os.environ.get("DATABASE_URL", DB_URL_DEFAULT)
conn = connect(DB_URL)
pq = PQ(conn)

# Set up logging.
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [clock.1]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Set up scheduler.
sched = BlockingScheduler()

JUDICIOUS_RECRUIT_INTERVAL = os.environ.get("JUDICIOUS_RECRUIT_INTERVAL", 10)

JUDICIOUS_CLEANUP_INTERVAL = os.environ.get("JUDICIOUS_CLEANUP_INTERVAL", 2)

recruiter_class_ = getattr(recruiters, os.environ["JUDICIOUS_RECRUITER"])
recruiter = recruiter_class_()


@sched.scheduled_job('interval', seconds=5)
def outstanding():
    logger.info("There are {} outstanding tasks.".format(len(pq['open'])))


@sched.scheduled_job('interval', seconds=JUDICIOUS_RECRUIT_INTERVAL)
def recruitment():
    logger.info('Running recruiter...')
    last_check = datetime.now() - timedelta(seconds=JUDICIOUS_RECRUIT_INTERVAL)
    num_new_tasks = Task.query.filter(Task.last_queued_at > last_check).count()
    logger.info("Found {} new tasks.".format(num_new_tasks))
    redundancy = int(os.environ.get("JUDICIOUS_REDUNDANCY", 1))
    for _ in range(num_new_tasks * redundancy):
        recruiter.recruit()


@sched.scheduled_job('interval', seconds=JUDICIOUS_CLEANUP_INTERVAL)
def cleanup():
    logger.info('Cleaning up task table...')
    # Timed out tasks have no result AND were last started over JUDICIOUS_TASK_TIMEOUT seconds ago.
    unfinished_tasks = Task.query\
        .filter_by(result=None)\
        .filter(Task.last_started_at.isnot(None))\
        .all()
    for task in unfinished_tasks:
        time_since = datetime.now() - task.last_started_at
        time_given = timedelta(
            seconds=int(os.environ['JUDICIOUS_TASK_TIMEOUT']))
        if time_since > time_given:
            task.timeout()


sched.start()
