#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial, SerialTimeoutException
import logging
from logging.handlers import RotatingFileHandler
from subprocess import PIPE, Popen
from animations import Led_clock_pointer, Led_clock_flasher
from lib import lcdControl
from lib import SevSeg

motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = .3

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
    # init virtual devices
    lcd = lcdControl.Lcd(usb)
    sevdp = SevSeg(usb)
    mtxdp = SevSeg(usb, dev_id=1)

    led_clock_pointer_sec = Led_clock_pointer(mtxdp, ring=1)
    led_clock_pointer_min = Led_clock_pointer(mtxdp, pointertype="min", ring=0)
    led_clock_flasher = Led_clock_flasher(mtxdp)

    lcd.push('clear')
    # turn on second display, > note: not sure why 0
    mtxdp.setstate(0)
    # set intensitive
    sevdp.setintensity(8)
    mtxdp.setintensity(0)
    # clear display
    sevdp.clear()
    mtxdp.clear()
    buf2 = b'\x00'


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

        # 8x8 LED matrix
        led_clock_pointer_sec.update()
        led_clock_pointer_min.update()
        led_clock_flasher.update()

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
        hour = time.time()/(60*60) % 24
        if(13 < hour < 21):
            lcd.backlight(0)
            mtxdp.setstate(1)
            sevdp.setstate(1)
        else:
            mtxdp.setstate(0)
            sevdp.setstate(0)
            lcd.backlight(1)

        # clock
        time.sleep(updateintv)
