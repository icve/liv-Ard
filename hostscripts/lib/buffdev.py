"""
a virtual usb device for buffering,
use for debugging purpose
"""
from json import dumps
from time import time


class Dev:
    def __init__(self, dev):
        self.buf = []
        self.dev = dev
        self.last_updated = None
        self.update_time = None

    def write(self, data):
        """ write data to buffer
            access .dev.write to write directly to device"""
        self.buf.append((time(), data))

    def read(self, b):
        """ read data , use .dev.read instead"""
        raise NotImplementedError("use .dev.read / .dev.write to read/write directly")

    def update(self):
        """ flush buffer and record time """
        for _, data in self.buf:
            self.dev.write(data)
        self.last_updated = self.update_time
        self.update_time = time()
        self.buf = []

    def get_json(self):
        """ dump buffer as json """
        return dumps([(t, [c for c in d])for t, d in self.buf])


