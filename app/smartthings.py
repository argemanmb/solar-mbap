#!/usr/bin/env python3

import requests
import json
import datetime
import time

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
        response = requests.post(apiUrl + self.id + "/commands", data=data, headers=self.header)
        if not response.status_code == 200:
            print ("resonse code wrong")
            print ( response.status_code )

    def activate(self):
        if(self.__active):
            return
        self.__active = True
        self.__saveStatus()
        self.setValues("on", self.targetHeat)

    def __saveStatus(self):
        self.__originalTemp = self.status.setPoint
        self.__originalState = self.status.switch

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
                    "arguments": [int(temperature)]
                }
            ]
        }
        print("executing COMMAND::: ")
        print(data)
        self.executeCommand(json.dumps(data))
        self.status.setPoint = temperature
        self.status.switch = state

    def updateStatus(self):
        response = requests.get(apiUrl + self.id+"/status", headers=self.header)
        if not response.status_code == 200:
            print ("resonse code wrong")
            print ( response.status_code )
        else:
            newStatus = smartthingsDeviceStatus(response.json())
            if(self.status is None or not self.status.isIdentical(newStatus)):
                self.lastManualInput = datetime.datetime.now()
            self.status = newStatus

    def printStatus(self):
        print("Temperature:" , self.status.temperature)
        print("Solltemperatur:" , self.status.setPoint)
        print("Schaltzustand:" , self.status.switch)

class smartthingsDeviceStatus:
    def __init__(self, statusJson):
        self.temperature = statusJson["components"]["main"]["temperatureMeasurement"]["temperature"]["value"]
        self.setPoint = statusJson["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"]
        self.switch = statusJson["components"]["main"]["switch"]["switch"]["value"]

    def isIdentical(self, newStatus):
        unchanged = True
        unchanged &= self.setPoint == newStatus.setPoint
        unchanged &= self.switch == newStatus.switch
        return unchanged
