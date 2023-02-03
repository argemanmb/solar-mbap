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

    def getStatus(self):
        response = requests.get(apiUrl+self.token+"&sn="+self.sn)
        if not response.status_code == 200:
            print ("something went wrong")
        else:
            self.status = response.json()
            return self.status

    def isFeedinHigh():
        if(self.feedinThreshold < self.status["result"]["feedinpower"]):
            if (self.feedInHighStart != None):
                if(self.minFeedInHighPhase < (datetime.datetime-self.feedInHighStart)):
                    return true
            else:
                self.feedInHighStart = datetime.datetime
        else:
            self.feedInHighStart = None
        return false
