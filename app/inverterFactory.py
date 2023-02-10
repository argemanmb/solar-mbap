#!/usr/bin/env python3

import qcells
import stubs.invTest

class inverterFactory:
    def __init__(self):
        pass

    def addDevice(self, deviceConfig):
        if(deviceConfig["type"] == "inverter"):
            return qcells.qcellDevice(deviceConfig)
        if(deviceConfig["type"] == "inverterStub"):
            return stubs.invTest.invTest(deviceConfig)
