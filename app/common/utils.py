# -*- coding: UTF-8 -*-

import threading
import time
from datetime import datetime


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class WorkerThread(threading.Thread):

    inc = -1
    action = None

    def __init__(self, inc, action):

        threading.Thread.__init__(self)
        self.inc = inc
        self.action = action

    def run(self):
        while True:
            # 每n秒执行一次
            self.action()
            time.sleep(self.inc)
