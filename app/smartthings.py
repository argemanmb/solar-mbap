#!/usr/bin/env python3

import requests
import json

apiUrl = "https://api.smartthings.com/v1/devices/"

class SmartthingDevice:
    def __init__(self, deviceID, deviceName, token):
        self.id = deviceID
        self.name = deviceName
        self.header = {"Authorization": "Bearer " + token}
        self.updateStatus()

    def executeCommand(self, data):
        requests.post(apiUrl + self.id + "/commands", data=data, headers=self.header)

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
        self.executeCommand(data)
        self.updateStatus()

    def updateStatus(self):
        response = requests.get(apiUrl + self.id+"/status", headers=self.header)
        if not response.status_code == 200:
            print ("resonse code wrong")
            print ( response.status_code )
        else:
            self.status = response.json()

    def printStatus(self):
        print(self.status["components"]["main"]["temperatureMeasurement"]["temperature"]["value"])
        print(self.status["components"]["main"]["thermostatCoolingSetpoint"]["coolingSetpoint"]["value"])
        print(self.status["components"]["main"]["switch"]["switch"]["value"])
