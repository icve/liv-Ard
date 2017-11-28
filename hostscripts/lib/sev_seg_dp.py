from .base.dev import Device

class Sev_seg_dp(Device):

    def __init__(self, dev, size=8, dev_id=0):
        self.buf = [""] * size
        self.is_shutdown = None
        self.dev = dev
        self.dev_id = dev_id
        super().__init__()

    def write(self, txt, pos=0, dot=0):
        """print text at pos"""
        if self.disable_flag:
            return
        for i, c in enumerate(reversed(txt)):
            # safe pos
            sp = (i + pos) % len(self.buf)
            if self.buf[sp] == txt[i]:
                continue
            else:
                data = "{}{}{}{}{};".format(chr(77),
                                            chr(self.dev_id),
                                            chr(sp),
                                            txt[i],
                                            chr(dot))
                self.dev.write(data.encode())
                # update buf
                self.buf[sp] = txt[i]

    def clear(self):
        """clear display"""
        data = "{}{};".format(chr(84), chr(self.dev_id))
        self.dev.write(data.encode())
        # clear buffer
        self.buf = [""]* len(self.buf)

    def printrow(self, row, hexval):
        """print hexval to row"""
        if self.disable_flag:
            return
        data = b"".join(i.to_bytes(1, 'big') for i in (79, self.dev_id, row, hexval)) + b';'
        self.dev.write(data)

    def printcol(self, col, hexval):
        """print hexval to col"""
        if self.disable_flag:
            return
        data = b"".join(i.to_bytes(1, 'big') for i in (80, self.dev_id, col, hexval)) + b';'
        self.dev.write(data)

    def setled(self, r, c, s):
        """set single lec"""
        if self.disable_flag:
            return
        data = "{}{}{}{}{};".format(chr(81), chr(self.dev_id), chr(r), chr(c), chr(s))
        self.dev.write(data.encode())

    def shutdown(self, s):
        """turn on/off the devide"""
        if self.is_shutdown != s:
            data = "{}{}{};".format(chr(82), chr(self.dev_id), chr(s))
            self.dev.write(data.encode())
            self.is_shutdown = s

    def setintensity(self, i):
        """set device off"""
        data = "{}{}{};".format(chr(83), chr(self.dev_id), chr(i))
        self.dev.write(data.encode())

    def disable(self):
        """disable device, turn off device and disable writing to usb"""
        self.shutdown(1)
        self.disable_flag = True

    def enable(self):
        """ re-enable device after disable"""
        self.shutdown(0)
        self.disable_flag = False
