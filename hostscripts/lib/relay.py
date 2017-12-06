
"""
relay module control
"""
CMD = bytes((85,))
ON = CMD + b'\x01;'
OFF = CMD + b'\x00;'


class Relay:

    def __init__(self, dev):
        self.dev = dev
        self.state = None

    def on(self):
        if self.state != True:
            self.dev.write(ON)
            self.state = True

    def off(self):
        if self.state != False:
            self.dev.write(OFF)
            self.state = False

    def get_state(self):
        return str(self.state)
