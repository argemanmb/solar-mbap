#!/usr/bin/env python3

import requests
apiUrl = "https://qhome-ess-g3.q-cells.eu/proxyApp/proxy/api/getRealtimeInfo.do?tokenId="

class qcellDevice:
    def __init__(self,token, sn):
        self.token=token
        self.sn=sn

    def GetStatus(self):
        response = requests.get(apiUrl+self.token+"&sn="+self.sn)
        if not response.status_code == 200:
            print ("something went wrong")
        else:
            return response.json()
