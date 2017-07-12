from subprocess import PIPE, Popen

TEMPPATH = "/sys/class/thermal/thermal_zone0/temp"
PITEMPLOG = "/mnt/usb/logs/piTem.log"


def get_temp():
    """ return temperature as int """
    with open(TEMPPATH, "r") as f:
        pitem = round(int(f.readline().replace("\n", "")) / 1000)
        return pitem


def get_netstat():
    """ return ping time to 8.8.8.8 as string e.g 16.221"""
    tail_cmd = ["tail", "-1", PITEMPLOG]
    last_line = Popen(tail_cmd, stdout=PIPE).communicate()[0].decode()
    netstat = last_line.split("\t")[-1].replace("\n", "")
    return netstat
