#!/mnt/usb/wk/jpt/py/bin/python

#TODO logging lib

import time
from serial import Serial
from sys import argv, exit

from lib.runner import Runner
from animations.matrix_animation import Led_clock_pointer, Led_clock_flasher
from lib import lcdControl
from lib.sev_seg_dp import Sev_seg_dp
from lib.motion_sensor import Motion_sensor
import lib.get_data as gdt
from animations.seven_segment_clock import Seven_segment_clock
from animations.rainfall import Rainfall
from animations.stat_show import single_slide, get_slides
from lib.relay import Relay
from lib.httpser import HttpSer
from lib.buffdev import Dev
from lib.current_sensor import Current_sensor
from lib.photo_resistor import Photo_resistor
from lib.notification_led import Notification_led


# SETTINGS
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
runner = Runner()
# init virtual devices
lcd = lcdControl.Lcd(usb)
sevdp = Sev_seg_dp(usb)
mtxdp = Sev_seg_dp(usb, dev_id=1)

runner.add_module(usb)

# led_clock_pointer_sec = Led_clock_pointer(mtxdp, ring=1)
# led_clock_pointer_min = Led_clock_pointer(mtxdp, pointertype="min", ring=0)
# led_clock_flasher = Led_clock_flasher(mtxdp)
runner.add_module(Seven_segment_clock(sevdp))
# seven_segment_clock = Seven_segment_clock(sevdp)

runner.add_module(Rainfall(mtxdp, max_height=6, max_speed=20, min_speed=10))
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
runner.add_module(lcd_stat_show)


# lazer notification
notification_led = Notification_led(usb)

# motion sensor
motion_sensor = Motion_sensor(usb.dev,
                              motionLogFile,
                              trigger_handlers=[notification_led.set_led])
# relay
relay = Relay(usb.dev)

current_sensor = Current_sensor(usb.dev)

photo_resistor = Photo_resistor(usb.dev)

def reset_mtx():
    usb.dev.write(bytes((87, ord(';'))))
    return "OK"

#api server
SERVE_MAP = {"/o": relay.on,
             "/f": relay.off,
             "/rs": relay.get_state,
             "/lo": notification_led.on,
             "/lf": notification_led.off,
             "/d": usb.get_json,
             "/c": current_sensor.get_json,
             "/p": photo_resistor.get_json,
             "/me": mtxdp.enable,
             "/md": mtxdp.disable,
             "/le": lcd.enable,
             "/ld": lcd.disable,
             "/reset": reset_mtx}

runner.add_module(HttpSer(SERVE_MAP, addr="0.0.0.0"))

mtxdp.shutdown(0)
sevdp.setintensity(8)
mtxdp.setintensity(0)

sevdp.clear()
mtxdp.clear()
lcd.clear()


def main():
    try:
        while True:
            runner.update()
            time.sleep(updateintv)
    except KeyboardInterrupt:
        apiser.close()
        print("\nport closed")
        exit(0)

if __name__ == "__main__":
    main()
