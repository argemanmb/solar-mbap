#!/usr/bin/env python3

import datetime

class wakeup:
    def __init__():
        pass

    def updateTime(time):
        with open("wakeuptime","w") as timeFile:
            timeFile.write(time.strftime("%Y%m%d%H%M%S"))
