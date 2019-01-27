from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
import requests

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Run ping to a specific server url to keep it alive (awake)
def ping():

    pingurl = os.environ.get('DOMAIN_URL') + '/ping'

    # TODO: Add error handling
    try:
        r = requests.get(pingurl)
    except:
        print("Unexpected error:", sys.exc_info())
    else:
        print('Ping {} at {}: {}'.format(pingurl, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), r.status_code))

sched = BlockingScheduler()

if os.environ.get('KEEP_ALIVE','0') ==  "1":
    try:
        every = int(os.environ.get('PING_EVERY_X_MINUTES','15'))
    except:
        every = 15
    print('Job: Add keepalive, running every {} minutes'.format(every))
    sched.add_job(ping, 'interval', minutes=every)

if len(sched.get_jobs()) > 0:
    sched.start()
