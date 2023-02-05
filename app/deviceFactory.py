#!/usr/bin/env python3

import smartthings

class deviceFactory:
    def __init__(self):
        pass

    def addDevice(self, token, deviceConfig):
        if(deviceConfig["type"] == "ac"):
            return smartthings.SmartthingDevice(token, deviceConfig)
