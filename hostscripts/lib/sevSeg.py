
class SevSeg:

    def __init__(self, dev, size=8, dev_id=0):
        self.buf = [""] * size
        self.onstate = None
        self.dev = dev
        self.dev_id = dev_id

    def write(self, txt, pos=0, dot=0):
        """print text at pos"""
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
        data = "{}{}{}{};".format(chr(79), chr(self.dev_id), chr(row), chr(hexval))
        self.dev.write(data.encode())

    def printcol(self, col, hexval):
        """print hexval to col"""
        data = "{}{}{}{};".format(chr(80), chr(self.dev_id), chr(col), chr(hexval))
        self.dev.write(data.encode())

    def setled(self, r, c, s):
        """set single lec"""
        data = "{}{}{}{}{};".format(chr(81), chr(self.dev_id), chr(r), chr(c), chr(s))
        self.dev.write(data.encode())

    def setstate(self, s):
        """turn on/off the devide"""
        if self.onstate != s:
            data = "{}{}{};".format(chr(82), chr(self.dev_id), chr(s))
            self.dev.write(data.encode())
            self.onstate = s

    def setintensity(self, i):
        """set device off"""
        data = "{}{}{};".format(chr(83), chr(self.dev_id), chr(i))
        self.dev.write(data.encode())
