#!/usr/bin/env python3

import json
import datetime
import time
import deviceFactory
import inverterFactory
import sys
import traceback
import wakeup


class controlConfig:
    def __init__(self, jsonData):
        self.devToken = jsonData["smartthings"]["token"]
        self.handsOffTime = jsonData["handsOffTime"]
        self.interval = jsonData["interval"]

class prioHandler:
    def __init__(self):
        self.prios = [-1]
        self.prioIndex = 0

    def addPrioLevel(self, prio):
        if(prio not in self.prios):
            self.prios.append(prio)
            self.prios.sort()

    def increasePrio(self):
        if(len(self.prios) > (self.prioIndex + 1)):
            self.prioIndex += 1

    def decreasePrio(self):
        if(self.prioIndex>0):
            self.prioIndex -= 1

    def getPrio(self):
        return self.prios[self.prioIndex]

logEntries = list()
logEntries.append(datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S.%f') + " system initialized")
if(len(sys.argv) > 1):
    configFile = arg1 = sys.argv[1]
else:
    configFile = "config.json"

with open(configFile) as configuration:
    jsonData = json.load(configuration)
config = controlConfig(jsonData)
factory = deviceFactory.deviceFactory()
handsoffTime = datetime.timedelta(minutes=int(config.handsOffTime))
devices = {}
prios = prioHandler()
for device in jsonData["smartthings"]["devices"]:
    prios.addPrioLevel(device["prio"])
    devices[device["name"]] = factory.addDevice(config.devToken, device)

qcellJson = jsonData["qcells"]["devices"][0]
inverterFactory = inverterFactory.inverterFactory()
wechselrichter = inverterFactory.addDevice(qcellJson)
print("Initialization successfull")

while(True):
    try:
        print(wechselrichter.getStatus())
        # waiting for some time, longer if the power is low...
        waitUntil = datetime.datetime.now() + datetime.timedelta(minutes=config.interval)
        if (wechselrichter.generatedPower < 1000):
            waitUntil = datetime.datetime.now() + datetime.timedelta(minutes=20)
        if (wechselrichter.generatedPower < 100):
            waitUntil = datetime.datetime.now() + datetime.timedelta(minutes=40)
        if (wechselrichter.generatedPower < 1):
            waitUntil = datetime.datetime.now() + datetime.timedelta(minutes=120)
        for dev in devices:
            # erstmal alle Informationen sammeln
            devices[dev].updateStatus()
            devices[dev].printStatus()

        print ("Power vom Dach:", wechselrichter.generatedPower)
        if(wechselrichter.isFeedinHigh()):
            oldPrio = prios.getPrio()
            prios.increasePrio()
            print("New prio:", prios.getPrio())
            if(oldPrio != prios.getPrio()):
                logEntries.append(datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S.%f') + " High input, change level to " + prios.getPrio())

        if(wechselrichter.isFeedinLow()):
            oldPrio = prios.getPrio()
            prios.decreasePrio()
            if(oldPrio != prios.getPrio()):
                logEntries.append(datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S.%f') + " Low input, change level to " + prios.getPrio())

        for dev in devices:
            noManualUpdates = devices[dev].isAvailable(handsoffTime)
            if(noManualUpdates):
                currentPrio = prios.getPrio()
                print("no manual updates, can do stuff!")
                if(devices[dev].prio <= currentPrio):
                    print("HIGH input, enable ac", dev)
                    devices[dev].activate()
                if (devices[dev].prio > currentPrio):
                    print("LOW input, deactivate ac", dev)
                    devices[dev].deactivate()
            else:
                print ("There were manual updates, need to keep hands off")
        print ("Done for now, continue at", waitUntil)
        #update status information in index.html
        with open("index.html", "w") as htmlFile:
            htmlFile.write("""<html>
<style>
table, th, td {
  border:1px solid black;
}
</style>
<body>
""")
            htmlFile.write("""<table style="width:100%">""")
            for dev in devices:
                htmlFile.write(devices[dev].getTableEntries(handsoffTime))
            htmlFile.write("</table><br/><br/><br/><br/>")
            htmlFile.write("Status " + datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S.%f') + "<br/><br/>")
            for entry in logEntries:
                htmlFile.write(entry + "<br/>")

        wakeup.wakeup.updateTime(waitUntil - datetime.timedelta(seconds=20))
        while(waitUntil > datetime.datetime.now()):
            time.sleep(1)
    except ConnectionError as e:
        print("connection issues")
        time.sleep(1)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print ( message )
        print(traceback.format_exc())
        print("exiting...")
        for dev in devices:
            try:
                devices[dev].deactivate()
            except:
                print("error while deacivating", dev)
        exit(0)
