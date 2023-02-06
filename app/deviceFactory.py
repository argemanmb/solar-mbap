#!/usr/bin/env python3

import smartthings
import stubs.acTest

class deviceFactory:
    def __init__(self):
        pass

    def addDevice(self, token, deviceConfig):
        if(deviceConfig["type"] == "ac"):
            return smartthings.SmartthingDevice(token, deviceConfig)
        if(deviceConfig["type"] == "acStub"):
            return stubs.acTest.acTest(token, deviceConfig)
