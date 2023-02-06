#!/usr/bin/env python3

import qcells

class inverterFactory:
    def __init__(self):
        pass

    def addDevice(self, deviceConfig):
        if(deviceConfig["type"] == "inverter"):
            return qcells.qcellDevice(deviceConfig)
