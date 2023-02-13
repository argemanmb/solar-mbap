#!/usr/bin/env python3

class invTest:
    def __init__(self, config):
       self.config = config
       self.fhcount = 0

    def getStatus(self):
        return "{}"

    def isFeedinHigh(self):
        if(self.config["feedInHigh"] == 1):
            return True
        if(self.config["feedInHigh"] == 2):
            self.fhcount +=1
            if(self.fhcount<10):
                return True
        return False

    def isFeedinLow(self):
        if(self.config["feedInLow"] == 1):
            return True
        if(self.config["feedInLow"] == 2):
            if(self.fhcount>20):
                if(self.fhcount>30):
                    raise Exception("passed")
                return True
        return False

    @property
    def generatedPower(self):
        return 10000
