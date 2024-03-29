#!/usr/bin/env python3

class acTest:
    def __init__(self, token, config):
        self.config = config
        self.active = False
        self.name = config["name"]
        self.prio = config["prio"]

    def activate(self):
        if(self.config["activateAllowed"]):
            self.active = True
            return
        else:
            raise Exception("fail: device wurde aktiviert:", self.config["name"])

    def deactivate(self):
        print("deactivate", self.name)
        self.active = False

    def updateStatus(self):
        pass

    def isAvailable(self, handsoffTime):
        return True

    def printStatus(self):
        pass

    def getTableEntries(self, handsoffTime):
        return "nothing"
