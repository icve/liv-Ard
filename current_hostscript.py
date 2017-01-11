#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial
import logging
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen

motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = .5

logger = logging.getLogger('mtlog')
handler = RotatingFileHandler(motionLogFile, maxBytes=50e3, backupCount=10)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s, %(message)s", datefmt="%d/%m/%y %X")
handler.setFormatter(formatter)

if __name__ == "__main__":
    logger.info("Starting")
    # Set up
    usb = Serial(device, baudrate)
    time.sleep(3)
    usb.write("0;".encode())
    usb.write("i8;".encode())
    # buffer for seven segment display
    buf = [0, 0, 0, 0, 0, 0, 0, 0]
    # buffer for led state
    buf2 = b'\x00'
    # main Loop
    while True:
        # seven segment display update
        pitem = 0
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            pitem = round(int(f.readline().replace("\n", "")) / 1000)
            netstat = Popen(["tail", "-1", "/mnt/usb/logs/piTem.log"], stdout=PIPE).communicate()[0].split("\t")[-1].replace("\n", "")
        for i, char in enumerate(reversed(time.strftime("{1}.%H{0}%M").format("-" if int(time.time()*2) % 2 == 0 else " ", int(pitem)))):
            if buf[i] != char:
                usb.write(("a" + str(i) + char + str(int(not i)) + ";").encode())
                usb.flush()
                buf[i] = char
        # motion Sensor ck
        usb.write(b'm;')
        state = usb.read(1)
        if state != buf2:
            logger.info(str(ord(state)))
            usb.write(b"b" + state + b";")
            buf2 = state
        time.sleep(updateintv)
