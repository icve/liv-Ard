"""
a virtual usb device for buffering
"""
from json import dumps
from time import time
class Dev:
    def __init__(self, dev):
        self.buf = []
        self.dev = dev
        self.last_updated = None
        self.update_time= None

    def write(self, data):
        """ write data to buffer"""
        # dont bufer when polling motion sensor
        if data[0] == 76:
            self.dev.write(data) 
            return
        self.buf.append((time(), data))

    def read(self, b):
        return self.dev.read(b)

    def update(self):
        """ flush buffer and record time """
        for _, data in self.buf:
            self.dev.write(data)
        self.last_updated = self.update_time
        self.update_time = time()
        self.buf = []

    def get_json(self):
        """ dump buffer as json """
        return dumps([(t, [c for c in d])for t,d in self.buf])


