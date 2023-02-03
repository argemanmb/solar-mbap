#!/usr/bin/env python3

import requests
import json
import datetime

apiUrl = "https://api.smartthings.com/v1/devices/"

class SmartthingDevice:
    def __init__(self, deviceID, deviceName, token, targetHeat, targetCool):
        self.status = None
        self.id = deviceID
        self.name = deviceName
        self.header = {"Authorization": "Bearer " + token}
        self.updateStatus()
        self.lastManualInput = datetime.datetime.now()
        self.targetHeat = targetHeat
        self.targetCool = targetCool
        self.__active = False

    def executeCommand(self, data):
        requests.post(apiUrl + self.id + "/commands", data=data, headers=self.header)

    def activate(self):
        if(self.__active):
            return
        self.__active = True
        self.__saveStatus()
        self.setValues("on", self.targetHeat)

    def __saveStatus(self):
        self.__originalTemp = self.status["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"]
        self.__originalState = self.status["components"]["main"]["switch"]["switch"]["value"]

    def deactivate(self):
        if(self.__active):
            self.setValues(self.__originalState, self.__originalTemp)
            self.__active = False

    def setValues(self, state, temperature):
        data = {
            "commands": [
                {
                    "component": "main",
                    "capability": "switch",
                    "command": state
                },
                {
                    "component": "main",
                    "capability": "thermostatCoolingSetpoint",
                    "command": "setCoolingSetpoint",
                    "arguments": [temperature]
                }
            ]
        }
        print("executing COMMAND::: ")
        print(data)
        self.executeCommand(data)
        self.updateStatus(True)

    def __isStatusChanged(self, newStatus):
        if(self.status is None):
            return True
        if((self.status["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"] ==
           newStatus["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"]) and
           (self.status["components"]["main"]["switch"]["switch"]["value"] ==
           newStatus["components"]["main"]["switch"]["switch"]["value"])):
            return False
        self.lastManualInput = datetime.datetime.now()
        return True

    def updateStatus(self, ignore=False):
        response = requests.get(apiUrl + self.id+"/status", headers=self.header)
        if not response.status_code == 200:
            print ("resonse code wrong")
            print ( response.status_code )
        else:
            newStatus = response.json()
            if(not ignore):
                self.__isStatusChanged(newStatus)
            self.status = newStatus

    def printStatus(self):
        print(self.status["components"]["main"]["temperatureMeasurement"]["temperature"]["value"])
        print(self.status["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"])
        print(self.status["components"]["main"]["switch"]["switch"]["value"])
