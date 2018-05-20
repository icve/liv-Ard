from subprocess import PIPE, Popen
from re import compile

TEMPPATH = "/sys/class/thermal/thermal_zone0/temp"
PITEMPLOG = "/mnt/usb/logs/piTem.log"
MEMFILE = "/proc/meminfo"


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
    try:
        return Popen(tail_cmd, stdout=PIPE).communicate()[0]\
                                           .decode()\
                                           .replace("\n", "")\
                                           .split("\t")[idx]
    except IndexError:
        return "ERR"


def get_uptime():
    c = compile(r"up\s+(.+)")
    s = Popen(["uptime"], stdout=PIPE).communicate()[0]\
                                      .decode()\
                                      .split(",")[0]
    return c.search(s).group(1)


def get_mem_usage(free=False):
    """ return memory usage in percentage
        agr: True for free, false for used"""
    r = compile(r"(\d+)\skB")
    # MemTotal:         948016 kB
    # MemFree:           32356 kB
    # MemAvailable:     527896 kB

    with open(MEMFILE, "r") as f:
        totall = f.readline()
        f.readline()
        availl = f.readline()

    if not (totall.startswith("MemTotal") and availl.startswith("MemAvailable")):
        raise IOError("memfile parse failed")
    total = int(r.search(totall).group(1))
    avail = int(r.search(availl).group(1))
    percentage = (avail / total if free else 1 - (avail / total)) * 100

    return "{:.2f}%".format(percentage)
