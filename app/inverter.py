#!/usr/bin/env python3

from abc import ABC, ABCMeta, abstractmethod

class inverter(ABC):
    @classmethod
    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    @abstractmethod
    def getStatus(self):
        pass

    @classmethod
    @abstractmethod
    def update(self, jsonData):
        pass

    @classmethod
    @abstractmethod
    def isFeedinHigh(self):
        pass


    @classmethod
    @abstractmethod
    def isFeedinLow(self):
        pass
