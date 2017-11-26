from json import dumps

class Current_sensor:
    """class for read and decoding the current sensor"""

    def __init__(self, dev):
        self.dev = dev

    def read(self):
        self.dev.write(bytes((86, ord(';'))))
        h = self.dev.read(1)
        l = self.dev.read(1)
        rlt = (ord(h) << 8) + ord(l)
        return rlt

    def get_json(self):
        return dumps({"c": self.read()}) 
