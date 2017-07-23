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
    return _tail_pi_tem(4)


def get_load():
    return _tail_pi_tem(2)

def get_package_lost():
    return _tail_pi_tem(3)

def _tail_pi_tem(idx):
    tail_cmd = ["tail", "-1", PITEMPLOG]
    return Popen(tail_cmd, stdout=PIPE).communicate()[0]\
                                       .decode()\
                                       .replace("\n", "")\
                                       .split("\t")[idx]
