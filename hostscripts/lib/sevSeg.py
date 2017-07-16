
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
                data = "a{}{}{}{};".format(self.dev_id, sp, txt[i], dot)
                self.dev.write(data.encode())
                # update buf
                self.buf[sp] = txt[i]

    def clear(self):
        """clear display"""
        data = "0{};".format(self.dev_id)
        self.dev.write(data.encode())
        # clear buffer
        self.buf = [""]* len(self.buf)

    def printrow(self, row, hexval):
        """print hexval to row"""
        data = "r{}{}{};".format(self.dev_id, row, hexval)
        self.dev.write(data.encode())

    def printcol(self, col, hexval):
        """print hexval to col"""
        data = "c{}{}{};".format(self.dev_id, col, hexval)
        self.dev.write(data.encode())

    def setled(self, r, c, s):
        """set single lec"""
        data = "l{}{}{}{};".format(self.dev_id, r, c, s)
        self.dev.write(data.encode())

    def setstate(self, s):
        """turn on/off the devide"""
        if self.onstate != s:
            data = "s{}{};".format(self.dev_id, s)
            self.dev.write(data.encode())
            self.onstate = s

    def setintensity(self, i):
        """set device off"""
        data = "i{}{};".format(self.dev_id, i)
        self.dev.write(data.encode())
