#!/usr/bin/env python3

import smartthings
import qcells
import json

with open("config.json") as configuration:
    jsonData = json.load(configuration)
    token = jsonData["smartthings"]["token"]
    devices = {}
    for device in jsonData["smartthings"]["devices"]:
        devices[device["name"]] = smartthings.SmartthingDevice(device["id"],device["name"], token)

    qcellJson = jsonData["qcells"]["devices"][0]
    wechselrichter = qcells.qcellDevice(qcellJson["token"], qcellJson["sn"])

    devices["wohnzimmer"].updateStatus()
    devices["wohnzimmer"].printStatus()

    print (wechselrichter.GetStatus())
