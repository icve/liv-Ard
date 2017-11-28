#!/mnt/usb/wk/jpt/py/bin/python

import time
from serial import Serial

from animations.matrix_animation import Led_clock_pointer, Led_clock_flasher
from lib import lcdControl
from lib.sev_seg_dp import Sev_seg_dp
from lib.motion_sensor import Motion_sensor
import lib.get_data as gdt
from animations.seven_segment_clock import Seven_segment_clock
from animations.rainfall import Rainfall
from sys import argv, exit
from animations.stat_show import single_slide, get_slides
from lib.relay import Relay
from lib.httpser import HttpSer
from lib.buffdev import Dev
from lib.current_sensor import Current_sensor


motionLogFile = "/mnt/usb/logs/motionLog.log"
device = "/dev/ttyUSB0"
baudrate = 9600
updateintv = 0.01
debug = "debug" in argv

print("update intv: {}".format(updateintv))

if updateintv != 0:
    print("or {} fps max".format(1 / updateintv))


# Set up usb
usb = Serial(device, baudrate, timeout=2)
usb = Dev(usb)
if debug:
    from test.usb_relay import Usb_relay
    usb = Usb_relay(usb)
time.sleep(3)
# init virtual devices
lcd = lcdControl.Lcd(usb)
sevdp = Sev_seg_dp(usb)
mtxdp = Sev_seg_dp(usb, dev_id=1)


# led_clock_pointer_sec = Led_clock_pointer(mtxdp, ring=1)
# led_clock_pointer_min = Led_clock_pointer(mtxdp, pointertype="min", ring=0)
# led_clock_flasher = Led_clock_flasher(mtxdp)
seven_segment_clock = Seven_segment_clock(sevdp)

rainfall = Rainfall(mtxdp, max_height=6, max_speed=20, min_speed=10)
# lcd_show_tem_net = single_slide("temp", get_temp, "ping", get_netstat, lcd)

lcd_stat_show = get_slides(lcd,
                           (("Temp", gdt.get_temp),
                            ("Up", gdt.get_uptime),
                            ("Load", gdt.get_load),
                            ("Mem", gdt.get_mem_usage),
                            ("Ping", gdt.get_netstat),
                            ("Lost", gdt.get_package_lost)),
                           update_every=3)

# devices that should not be buffered
# motion sensor
moss = Motion_sensor(usb.dev, motionLogFile)
# relay
relay = Relay(usb.dev)

current_sensor = Current_sensor(usb.dev)

def reset_mtx():
    usb.dev.write(bytes((87, ord(';'))))
    return "OK"

#api server
SERVE_MAP = {"/o": relay.on,
             "/f": relay.off,
             "/d": usb.get_json,
             "/c": current_sensor.get_json,
             "/me": mtxdp.enable,
             "/md": mtxdp.disable,
             "/le": lcd.enable,
             "/ld": lcd.disable,
             "/reset": reset_mtx}

apiser = HttpSer(SERVE_MAP, addr="0.0.0.0")

mtxdp.shutdown(0)
sevdp.setintensity(8)
mtxdp.setintensity(0)

sevdp.clear()
mtxdp.clear()
lcd.clear()


def main():
    try:
        while True:
            update()
            # clock
            time.sleep(updateintv)
    except KeyboardInterrupt:
        apiser.close()
        print("\nport closed")
        exit(0)


def update():
    """ functions to run on every update """
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
    # lcd_show_tem_net.show()
    lcd_stat_show.update()

    # on off cycle
    hour = time.time()/(60*60) % 24
    if 13 < hour < 21 and not debug:
        lcd.backlight(0)
        mtxdp.shutdown(1)
        sevdp.shutdown(1)
    else:
        mtxdp.shutdown(0)
        sevdp.shutdown(0)
        lcd.backlight(1)
    apiser.update()
    usb.update()


main()
