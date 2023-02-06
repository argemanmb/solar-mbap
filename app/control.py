#!/usr/bin/env python3

import json
import datetime
import time
import deviceFactory
import inverterFactory

with open("config.json") as configuration:
    jsonData = json.load(configuration)
    factory = deviceFactory.deviceFactory()
    token = jsonData["smartthings"]["token"]
    handsoffTime = datetime.timedelta(minutes=int(jsonData["handsOffTime"]))
    devices = {}
    prios = []
    for device in jsonData["smartthings"]["devices"]:
        prio = device["prio"]
        if(prio not in prios):
            prios.append(prio)
        devices[device["name"]] = factory.addDevice(token, device)

    prios.sort()
    priolevels = len(prios)
    currentPrioIndex = -1
    qcellJson = jsonData["qcells"]["devices"][0]
    inverterFactory = inverterFactory.inverterFactory()
    wechselrichter = inverterFactory.addDevice(qcellJson)

    print("Initialization successfull")
    while(True):
        try:
            print(wechselrichter.getStatus())
            waitUntil = datetime.datetime.now() + datetime.timedelta(minutes=5)
            for dev in devices:
                devices[dev].updateStatus()
                devices[dev].printStatus()

            if(wechselrichter.isFeedinHigh() and currentPrioIndex < priolevels):
                currentPrioIndex += 1
            if(wechselrichter.isFeedinLow() and currentPrioIndex > -1):
                currentPrioIndex -= 1

            for dev in devices:
                noManualUpdates = devices[dev].isAvailable(handsoffTime)
                if(noManualUpdates):
                    print("no manual updates, can do stuff!")
                    if(wechselrichter.isFeedinHigh() and device[dev].prio >= prios[currentPrioIndex]):
                        print("HIGH input, enable ac")
                        devices[dev].activate()
                    if (device[dev].prio < prios[currentPrioIndex]):
                        print("LOW input, deactivate ac")
                        devices[dev].deactivate()
                else:
                    print ("There were manual updates, need to keep hands off")
            print ("Done for now, continue at", waitUntil)
            while(waitUntil > datetime.datetime.now()):
                time.sleep(1)
        except ConnectionError as e:
            print("connection issues")
            time.sleep(1)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print ( message )
            print("exiting...")
            for dev in devices:
                try:
                    devices[dev].deactivate()
                except:
                    print("error while deacivating", dev)
                exit(0)
