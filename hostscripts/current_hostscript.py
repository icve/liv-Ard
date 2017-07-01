#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial, SerialTimeoutException
import logging
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen
from animations import ledClockPointer
from lib import lcdControl
from lib import SevSeg
motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = .5
ledpointer = ledClockPointer()

logger = logging.getLogger('mtlog')
handler = RotatingFileHandler(motionLogFile, maxBytes=50e3, backupCount=10)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s, %(message)s", datefmt="%d/%m/%y %X")
handler.setFormatter(formatter)

if __name__ == "__main__":
    logger.info("Starting")
    # Set up
    usb = Serial(device, baudrate, timeout=2)
    time.sleep(3)
    # lcd init
    lcd = lcdControl.Lcd(usb)
    sevdp = SevSeg(usb)
    mtxdp = SevSeg(usb, dev_id=1)
    lcd.push('clear')
    # turn on second display, > note: not sure why 0
    ## usb.write("s10;".encode())
    mtxdp.setstate(0)
    # set intensitive
    ## usb.write("i08;".encode())
    sevdp.setintensity(8)
    ## usb.write("i11;".encode())
    mtxdp.setintensity(0)
    # clear display
    ## usb.write("00;".encode())
    ## usb.write("01;".encode())
    sevdp.clear()
    mtxdp.clear()
    # buffer for seven segment display
    ## buf = [0, 0, 0, 0, 0, 0, 0, 0]
    # buffer for led state
    buf2 = b'\x00'
    # buffer for matric led pointer animation
    lastled = 0
    # main Loop
    while True:
        # seven segment display update
        pitem = 0
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            pitem = round(int(f.readline().replace("\n", "")) / 1000)
            netstat = Popen(["tail", "-1", "/mnt/usb/logs/piTem.log"], stdout=PIPE).communicate()[0].decode().split("\t")[-1].replace("\n", "")
        for i, char in enumerate(reversed(time.strftime("{1}.%H{0}%M").format("-" if int(time.time()*2) % 2 == 0 else " ", int(pitem)))):
            sevdp.write(char, i)
            """
            if buf[i] != char:
                usb.write(("a" + "0" + str(i) + char + str(int(not i)) + ";").encode())
                # usb.write(("r" + "1" + "0" +("FF" if int(round(time.time())) % 2 else "00") + ";").encode())
                usb.flush()
                buf[i] = char
            """

        led = int(time.time()%60/59 * 27)
        if led != lastled:
            if(led)==0:
                mtxdp.clear()
            # turn on current new led
            usb.write(("l1" + "".join(ledpointer.ledRing[led]) + "1" + ";").encode())
            # turn off last led
            ## usb.write(("l1" + "".join(ledpointer.ledRing[lastled]) + "0" + ";").encode())
            lastled = led
        # motion Sensor ck
        usb.write(b'm;')
        state = usb.read(1)
        if state != buf2:
            logger.info(str(ord(state)))
            usb.write(b"b" + state + b";")
            buf2 = state
        # lcd
        lcd.setCursor(0, 0)
        lcd.print(time.strftime("%d/%m/%y"))
        lcd.setCursor(0, 1)
        lcd.print(time.strftime("%X"))
        hour = time.time()/(60*60)% 24
        if(13 < hour < 21):
            lcd.backlight(0)
        else:
            lcd.backlight(1)

        # clock
        time.sleep(updateintv)

