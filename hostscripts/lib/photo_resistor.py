
from .util import join_byte
from json import dumps

class Photo_resistor:

    def __init__(self, dev):
        self.dev = dev

    def read(self):
        dev = self.dev
        cmd = (88, ord(';'))
        dev.write(bytes(cmd))
        return join_byte(dev.read(1), dev.read(1))

    def get_json(self):
        return dumps({"p": self.read()})
        

