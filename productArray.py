from product import *
from m_email import *
from m_text import *

class productArray:
    def __init__(self):
        self.array = []
        self.statArray = []

    def add(self, object):
        self.array.append(object)

    def getStats(self):
        self.statArray.clear()
        for object in self.array:
            self.statArray.append(object.getStat())
            if object.avaliable:
                sendEmail(object.toString())
                sendSMS(object.toString())

        return self.statArray

    def remove(self, url):
        for idx, object in enumerate(self.array):
            if object.m_url == url:
                self.array.pop(idx)