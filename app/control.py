#!/usr/bin/env python3

import smartthings
import qcells
import json
import datetime
import time

with open("config.json") as configuration:
    jsonData = json.load(configuration)
    token = jsonData["smartthings"]["token"]
    handsoffTime = datetime.timedelta(minutes=int(jsonData["handsOffTime"]))
    devices = {}
    for device in jsonData["smartthings"]["devices"]:
        deviceId = device["id"]
        targetHeat = device["targetTempHeating"]
        targetCool = device["targetTempCooling"]
        devices[device["name"]] = smartthings.SmartthingDevice(deviceId, device["name"], token, targetHeat, targetCool)

    qcellJson = jsonData["qcells"]["devices"][0]
    feedInDelta = datetime.timedelta(minutes=int(qcellJson["feedInHighMinutes"]))
    wechselrichter = qcells.qcellDevice(qcellJson["token"], qcellJson["sn"], qcellJson["feedInThreshold"], feedInDelta)

    while(True):
        print(wechselrichter.getStatus())
        for dev in devices:
            devices[dev].updateStatus()
            devices[dev].printStatus()
            noManualUpdates = (datetime.datetime.now() - devices[dev].lastManualInput) > handsoffTime
            if(noManualUpdates):
                print("no manual updates, can do stuff!")
                if(wechselrichter.isFeedinHigh()):
                    print("HIGH input, enable ac")
                    devices[dev].activate()
                else:
                    print("LOW input, no ac")
                    devices[dev].deactivate()
            else:
                print ("There were manual updates, need to keep hands off\n")
        time.sleep(300)
