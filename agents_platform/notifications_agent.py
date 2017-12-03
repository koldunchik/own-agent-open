import json
import re
import threading
import time
import traceback

import logger, pprint
from own_adapter.agent import Agent
from own_adapter.board import Board
from own_adapter.element import Element
from own_adapter.platform_access import PlatformAccess, get_agent
from datetime import datetime, timedelta

# Notify X minutes before deadline
DEADLINE_MINUTES = 30

# Notify Y days before deadline
DEADLINE_DAYS = 1

def run():
    notification_status = {}

    while True:
        # periodical updates

        agent = get_agent()
        platform_access = agent.get_platform_access()

        boards = agent.get_boards()

        time.sleep(3)

        for board in boards:
            name = board.get_name()
            print (name)
            if name.lower() != 'Student Board'.lower():
                continue;
            elements = board.get_elements()
            for element in elements:
                ename = element.get_name()
                if not ename.startswith("@assignment"):
                    continue

                print ("ename:" + ename)
                m = re.search('\d{2,4}-\d{1,2}-\d{1,2}\s+\d{1,2}\:\d{1,2}', ename)
                if not m:
                    print ("notificator:invalid format ")
                    continue

                alert_date = m.group(0)
                datetime_minutes = datetime.strptime(alert_date, '%Y-%m-%d %H:%M') - timedelta(minutes = DEADLINE_MINUTES)
                datetime_days = datetime.strptime(alert_date, '%Y-%m-%d %H:%M') - timedelta(days = DEADLINE_DAYS)

                if datetime.now() >= datetime_minutes or datetime.now() >= datetime_days:
                    nstatus = notification_status.get(ename)
                    if nstatus != None:
                        if nstatus >= datetime_minutes:
                            continue

                    print (datetime_minutes)
                    print (datetime_days)
                    board.put_message("Attention! Deadline is soon for " + ename + " Think about it!")
                    notification_status[ename] = datetime.now()
                    print ("notification sent")

        print ("round")

        # wait until next check
        time.sleep(1000)


if __name__ == '__main__':
    run()
