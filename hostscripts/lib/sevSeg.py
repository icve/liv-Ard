
class SevSeg:

    def __init__(self, dev, size=8, dev_id=0):
        self.buf = [""] * size
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
                data = "a{dv}{dg}{ch}{.};".format(
                    {"dv": self.dev_id,
                     "dg": sp,
                     "ch": txt[i],
                     ".": dot}
                )
                self.dev.write(data.encode())
                # update buf
                self.buf[sp] = txt[i]

    def clear(self):
        """clear display"""
        data = "0{};".format(self.dev_id)
        self.dev.write(data.encode())

    def printrow(self, hexval):
        """print hexval to row"""
        data = "r{}{};".format(self.dev_id, hexval)
        self.dev.write(data.encode())

    def printcol(self, hexval):
        """print hexval to col"""
        data = "c{}{};".format(self.dev_id, hexval)
        self.dev.write(data.encode())

    def setled(self, r, c, s):
        """set single lec"""
        data = "l{}{}{}{};".format(self.dev_id, r, c, s)
        self.dev.write(data.encode())

    def setstate(self, s):
        """turn on/off the devide"""
        data = "s{}{};".format(self.dev_id, s)
        self.dev.write(data.encode())

    def setintensity(self, i):
        """set device off"""
        data = "i{}{};".format(self.dev_id, i)
        self.dev.write(data.encode())
