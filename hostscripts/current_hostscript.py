#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial
from animations.matrix_animation import Led_clock_pointer, Led_clock_flasher
from lib import lcdControl
from lib.sevSeg import SevSeg
from lib.motion_sensor import Motion_sensor
import lib.get_data as gdt
from animations.seven_segment_clock import Seven_segment_clock
from animations.rainfall import Rainfall
from sys import argv
from animations.stat_show import single_slide, get_slides


motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = 0.01
debug = "debug" in argv

print("update intv: {}".format(updateintv))

if updateintv != 0:
    print("or {} fps max".format(1 / updateintv))

if __name__ == "__main__":

    # Set up usb
    usb = Serial(device, baudrate, timeout=2)
    if debug:
        from test.usb_relay import Usb_relay
        usb = Usb_relay(usb)
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

    # rainfall = Rainfall(mtxdp, max_height=6, max_speed=20, min_speed=10)
    # lcd_show_tem_net = single_slide("temp", get_temp, "ping", get_netstat, lcd)

    lcd_stat_show = get_slides(lcd,
                               (("Temp", gdt.get_temp),
                                ("Up", gdt.get_uptime),
                                ("Load", gdt.get_load),
                                ("Mem", gdt.get_mem_usage),
                                ("Ping", gdt.get_netstat),
                                ("Lost", gdt.get_package_lost)),
                               update_every=3)

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
        # rainfall.update()

        # motion Sensor ck
        moss.update()
        # lcd
        # lcd_show_tem_net.show()
        lcd_stat_show.update()

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
