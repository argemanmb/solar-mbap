#!/usr/bin/env python3

import smartthings
import qcells
import json
import datetime

with open("config.json") as configuration:
    jsonData = json.load(configuration)
    token = jsonData["smartthings"]["token"]
    handsoffTime = datetime.timedelta(minutes=jsonData["handsOffTime"])
    devices = {}
    for device in jsonData["smartthings"]["devices"]:
        devices[device["name"]] = smartthings.SmartthingDevice(device["id"],device["name"], token)

    qcellJson = jsonData["qcells"]["devices"][0]
    wechselrichter = qcells.qcellDevice(qcellJson["token"], qcellJson["sn"], qcellJson["feedInThreshold"], datetime.timedelta(minutes=qcellJson["feedInHighMinutes"]))

    wechselrichter.getStatus()
    for dev in devices:
        devices[dev].updateStatus()
        if(datetime.datetime.now - devices[dev].lastManualInput > handsoffTime):
            if(wechselrichter.isFeedinHigh()):
                devices[dev].activate()
            else:
                devices[dev].deactivate()
