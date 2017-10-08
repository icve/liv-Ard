

from sys import argv
from serial import Serial

def gs(i):
    port = "/dev/ttyUSB" + i
    return Serial(port=port , baudrate=9600)

s = gs(argv[1])

opt = chr(78) + "0111;"

