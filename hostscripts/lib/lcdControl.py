

class Lcd:

    def __init__(self, dev, cmdmap="", size=(16, 2), bufsize=40, curpos=0, scpos=0, lcdParsecmd='x', printOverHead=8):
        self.dev = dev
        self.size = size
        self.lcdParsecmd = lcdParsecmd
        # printOverHead are used to determine whether to split print cmd when there is gap between txt cluster
        self.printOverHead = printOverHead
        self.bufsize = bufsize
        self.curpos = curpos
        self.scpos = scpos
        self.lightstate = None
        # create buffer
        self._setup_buffer()
        if cmdmap == "":
            self.cmdmap = {
                "setCursor": 32,
                "print": 33,
                "backlight": 34,
                "noBacklight": 35,
                "blink": 36,
                "noBlink": 37,
                "cursor": 38,
                "noCursor": 39,
                "clear": 40,
                "home": 41,
                "moveCursorLeft": 42,
                "moveCursorRight": 43,
                "autoscroll": 44,
                "noAutoscroll": 45,
                "on": 46,
                "off": 47,
                "display": 48,
                "noDisplay": 49,
                "scrollDisplayLeft": 50,
                "scrollDisplayRight": 51,
                # curpos update not yet implemented
                "leftToRight": 52,
                "rightToLeft": 53}
        else:
            self.cmdmap = cmdmap

    def rpush(self, rcmd):
        '''Does not advise user to use since this skips the cursor update'''
        cmd = self.lcdParsecmd + chr(rcmd) + ";"
        self.dev.write(cmd.encode())

    def push(self, ky):
        self.rpush(self.cmdmap[ky])
        if ky in ["clear", "home"]:
            self.updcur(0, True)
            return
        if ky == "moveCursorLeft":
            self.updcur(-1)
            return
        if ky == "moveCursorRight":
            self.updcur(1)
            return

    def setCursor(self, c, r):
        # displace to avoid transmitting 0, as weirdness occurs on rpi-ard when 0 is send?
        # please alos see the ard sketch for dedisplacement
        self.dev.write(("x" + chr(32) + chr(c + 1) + chr(r + 1) + ";").encode())
        self.updcur([c, r], True)

    def rprint(self, txt):
        '''Directly prints text to display without diff'''
        self.dev.write((self.lcdParsecmd + chr(self.cmdmap["print"]) + txt + ";").encode())
        for i, char in enumerate(txt):
            c, r = self.convpos(i + self.curpos)
            self.buf[r][c] = char
        self.updcur(len(txt))

    def getBuf(self, dig):
        '''get char in buf at position (number not coordinate)'''
        c, r = self.convpos(dig)
        return self.buf[r][c]

    def dPrint(self, txt):
        '''diff/delta print'''
        txtCluster = []
        clusterPos = []
        i = 0
        while i < len(txt):
            c, r = self.convpos(i + self.curpos)
            # new cluster
            if self.buf[r][c] != txt[i]:
                clusterPos.append([c, r])
                # for storng diff char
                temptxt = []
                temptxt.append(txt[i])
                i += 1
                gap = 0

                # examine cluster and count gap
                while gap < self.printOverHead and i < len(txt):
                    c, r = self.convpos(i + self.curpos)
                    if self.buf[r][c] != txt[i]:
                        temptxt.append(txt[i])
                        i += 1
                    else:
                        gap = 0
                        gaptxt = []
                        # discard flag
                        discard = False
                        while not discard:
                            if (not i < len(txt)) or gap >= self.printOverHead:
                                discard = True
                                break
                            elif self.getBuf(i + self.curpos) != txt[i]:
                                break
                            else:
                                gaptxt.append(txt[i])
                            i += 1
                            gap += 1
                        if not discard:
                            temptxt = temptxt + gaptxt

                txtCluster.append("".join(temptxt))
            # continue to find cluster
            else:
                i += 1
        return clusterPos, txtCluster

    def print(self, txt):
        '''method that calls the dprint and rprint'''
        cood, txts = self.dPrint(txt)

        if len(cood) != len(txts):
            raise IndexError("cood and txts does not match")
        if len(cood) == 0:
            # print("no-op")
            return
        for c, t in zip(cood, txts):
            rw, cl = c
            if not self.convpos([rw, cl]) == self.curpos:
                self.setCursor(rw, cl)
                # print("s: {}".format([rw, cl]))

            self.rprint(t)
            # print("p: {}".format(t))

    def updcur(self, val, raw=False):
        'flag raw to set instead of displace curpos'
        if type(val) is list:
            val = self.convpos(val)
        if raw:
            self.curpos = val
            return
        else:
            rval = val + self.curpos
            totalbuf = self.bufsize * self.size[1]
            # modding works for both pos and neg val
            self.curpos = rval % totalbuf

    def convpos(self, curpos):
        if type(curpos) is list:
            return curpos[0] + curpos[1] * self.bufsize
        elif type(curpos) is int:
            return [curpos % self.bufsize, int(curpos / self.bufsize)]

    def backlight(self, i):
        """ turn on / off backlight"""
        if self.lightstate != i:
            if i:
                self.push("backlight")
            else:
                self.push("noBacklight")
            self.lightstate = i

    def clear(self):
        """clear display and buffer"""
        self._setup_buffer()
        self.push("clear")

    def _setup_buffer(self):
        self.buf = [[" " for c in range(self.bufsize)] for r in range(self.size[1])]
