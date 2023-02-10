#!/usr/bin/env python3

import requests
import datetime
apiUrl = "https://qhome-ess-g3.q-cells.eu/proxyApp/proxy/api/getRealtimeInfo.do?tokenId="

class inverterStatus:
    def __init__(self):
        pass


    def update(jsonData):
        self.data = jsonData
        self.feedInPower = jsonData["result"]["feedinpower"]
        self.batPower = jsonData["result"]["batPower"]
class qcellDevice:
    def __init__(self, qcellJson):
        self.token = qcellJson["token"]
        self.sn = qcellJson["sn"]
        self.minFeedInHighPhase = datetime.timedelta(minutes=int(qcellJson["feedInHighMinutes"]))
        self.feedInThreshold = qcellJson["feedInThreshold"]
        self.feedInHighStart = None
        self.feedInLowStart = None
        self.status = inverterStatus()

    def getStatus(self):
        try:
            response = requests.get(apiUrl+self.token+"&sn="+self.sn)
        except:
            raise ConnectionError
        if not response.status_code == 200:
            print ("something went wrong")
            raise ConnectionError
        else:
            self.status.update(response.json())
            return response.json()

    def isFeedinHigh(self):
        if(float(self.feedInThreshold) < self.status.feedInPower):
            if (self.feedInHighStart != None):
                if(self.minFeedInHighPhase < (datetime.datetime.now() - self.feedInHighStart)):
                    return True
            else:
                self.feedInHighStart = datetime.datetime.now()
        else:
            self.feedInHighStart = None
        return False

    def isFeedinLow(self):
        if((self.status.feedInPower + self.status.batPower) < 0):
            return True
        return False
