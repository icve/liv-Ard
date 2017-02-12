from serial import Serial
from time import sleep


class Lcd:

    def __init__(self, dev, cmdmap="", size=(16, 2), bufsize=40, curpos=0, scpos=0, lcdParsecmd='x'):
        self.dev = dev
        self.size = size
        self.lcdParsecmd = lcdParsecmd
        # create buffer
        self.buf = [[" " for c in range(size[0])] for r in range(size[1])]
        self.bufsize = bufsize
        self.curpos = curpos
        self.scpos = scpos
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
                "leftToRight": 52,
                "rightToLeft": 53}
        else:
            self.cmdmap = cmdmap

    def rpush(self, rcmd):
        '''Does not advise user to use since this skips the cursor update'''
        if type(rcmd) is int:
            cmd = self.lcdParsecmd + chr(rcmd) + ";"
        else:
            # for setCursor
            cmd = self.lcdParsecmd + "".join(map(chr, rcmd)) + ";"
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
        # self.rpush([self.cmdmap["setCursor"], c, r])
        # displace to avoid transmitting 0, as weirdness occurs on rpi-ard when 0 is send?
        # please alos see the ard sketch for dedisplacement
        self.dev.write(("x" + chr(32) + chr(c + 1) + chr(r + 1) + ";").encode())
        self.updcur([c, r], True)

    def print(self, txt):
        self.dev.write((self.lcdParsecmd + chr(self.cmdmap["print"]) + txt + ";").encode())
        self.updcur(len(txt))

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

# usb = Serial("/dev/ttyUSB0")
# lcd = Lcd(usb)

# sleep(3)
# lcd.push("sensor")
# p = "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
# p = "3.141592653589793238462643383279502884193.14159265358979323846264338327950288419"
# p = "3.14159265358979323846264338327950288419"
# lcd.print(p)
# # lcd.setCursor(5, 1)
# # print(lcd.curpos)

# import time
# lcd.setCursor(0, 1)
# sleep(1)
# lcd.push("clear")
# while True:
#     sleep(.5)
#     lcd.setCursor(0, 0)
#     lcd.print(time.strftime("%x"))
#     lcd.setCursor(0, 1)
#     lcd.print(time.strftime("%X"))

