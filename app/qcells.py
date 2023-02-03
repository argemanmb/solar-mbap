#!/usr/bin/env python3

import requests
import datetime
apiUrl = "https://qhome-ess-g3.q-cells.eu/proxyApp/proxy/api/getRealtimeInfo.do?tokenId="

class qcellDevice:
    def __init__(self,token, sn, feedInThreshold, minFeedInHighPhase):
        self.token=token
        self.sn=sn
        self.feedInThreshold = feedInThreshold
        self.minFeedInHighPhase = minFeedInHighPhase
        self.feedInHighStart = None

    def getStatus(self):
        response = requests.get(apiUrl+self.token+"&sn="+self.sn)
        if not response.status_code == 200:
            print ("something went wrong")
        else:
            self.status = response.json()
            return self.status

    def isFeedinHigh(self):
        if(float(self.feedInThreshold) < self.status["result"]["feedinpower"]):
            if (self.feedInHighStart != None):
                if(self.minFeedInHighPhase < (datetime.datetime.now() - self.feedInHighStart)):
                    return True
            else:
                self.feedInHighStart = datetime.datetime.now()
        else:
            self.feedInHighStart = None
        return False
