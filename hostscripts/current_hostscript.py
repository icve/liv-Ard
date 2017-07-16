#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial
from animations import Led_clock_pointer, Led_clock_flasher
from lib import lcdControl
from lib import SevSeg
from lib import Motion_sensor
from lib.get_data import get_temp, get_netstat
from animations import Seven_segment_clock, Rainfall
from sys import argv


motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = .5
debug = "debug" in argv

print("update intv: {}".format(updateintv))


if __name__ == "__main__":

    # Set up usb
    usb = Serial(device, baudrate, timeout=2)
    time.sleep(3)
    # init virtual devices
    lcd = lcdControl.Lcd(usb)
    sevdp = SevSeg(usb)
    mtxdp = SevSeg(usb, dev_id=1)
    moss = Motion_sensor(usb, motionLogFile)

    # led_clock_pointer_sec = Led_clock_pointer(mtxdp, ring=1)
    # led_clock_pointer_min = Led_clock_pointer(mtxdp, pointertype="min", ring=0)
    # led_clock_flasher = Led_clock_flasher(mtxdp)
    seven_segment_clock = Seven_segment_clock(sevdp)

    rainfall = Rainfall(mtxdp, 2)

    # turn on second display, > note: not sure why 0
    mtxdp.setstate(0)
    sevdp.setintensity(8)
    mtxdp.setintensity(0)

    sevdp.clear()
    mtxdp.clear()
    lcd.clear()

    while True:
        # seven_segment_clock update
        seven_segment_clock.update()

        # 8x8 LED matrix
        # led_clock_pointer_sec.update()
        # led_clock_pointer_min.update()
        # led_clock_flasher.update()
        rainfall.update()

        # motion Sensor ck
        moss.update()
        # lcd
        netstat = get_netstat()
        temp = get_temp()
        lcd.setCursor(0, 0)
        lcd.print("tmp: {}".format(temp))
        lcd.setCursor(0, 1)
        lcd.print("net: {}".format(netstat.ljust(11, " ")))
        # on off cycle
        hour = time.time()/(60*60) % 24
        if(13 < hour < 21 and not debug):
            lcd.backlight(0)
            mtxdp.setstate(1)
            sevdp.setstate(1)
        else:
            mtxdp.setstate(0)
            sevdp.setstate(0)
            lcd.backlight(1)

        # clock
        time.sleep(updateintv)
