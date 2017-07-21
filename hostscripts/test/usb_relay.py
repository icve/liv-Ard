from animations.base.update_wait import Update_wait


class Usb_relay(Update_wait):
    """relay for debug
    print out to screen and send
    counts byte per second"""
    def __init__(self, usb, ifprintcmd=False, ifcount=True, sample_for=60):
        super().__init__(sample_for)
        self.usb = usb
        self.byte_count = 0
        self.ifprintcmd = ifprintcmd
        self.ifcount = ifcount
        if ifcount:
            print("counting byte per sec")
            print("sample for {} sec(s)".format(sample_for))
        if ifprintcmd:
            print("printing cmds")

    def read(self, i):
        self.printcmd("read")
        self.count_byte(1)
        return self.usb.read(i)
        return b'\x01'

    def write(self, s):
        self.printcmd([s.decode()])
        self.usb.write(s)

        self.count_byte(len(s))

    def count_byte(self, n):
        if not self.ifcount:
            return
        self.byte_count += n
        # preserve last update time
        last_updated = self.last_updated
        if self.iftimeout():
            byte_per_sec = self.byte_count / (self.last_updated - last_updated)
            print(byte_per_sec)
            self.byte_count = 0

    def printcmd(self, s):
        if not self.ifprintcmd:
            return
        print(s)
