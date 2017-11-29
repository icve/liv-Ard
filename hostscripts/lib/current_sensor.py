from json import dumps
from .util import join_byte

class Current_sensor:
    """class for read and decoding the current sensor"""

    def __init__(self, dev):
        self.dev = dev

    def read(self):
        self.dev.write(bytes((86, ord(';'))))
        h = self.dev.read(1)
        l = self.dev.read(1)
        return join_byte(h, l)

    def get_json(self):
        return dumps({"c": self.read()}) 
