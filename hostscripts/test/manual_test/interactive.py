

from sys import argv
from serial import Serial

class T:
    def __init__(self, dev, pref="", surf=";"):
        self.dev = dev
        self.pref = pref
        self.surf = surf

    def s(self, pl):
        pl = "{}{}{}".format(self.pref, pl, self.surf)
        print([pl])
        self.dev.write(pl.encode())

def gs(i):
    port = "/dev/ttyUSB" + i
    return T(Serial(port=port , baudrate=9600))

def gb(*arr):
    return "".join([chr(a) for a in arr])


s = gs(argv[1])

print("s.s(pl) write to usb")
print("s.pref sets msg prefix")
print("s.surf sets msg surfix")
print("gb(arr) gets byte string")

