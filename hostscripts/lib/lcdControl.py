from serial import Serial
from time import sleep


class Lcd:

    def __init__(self, dev, cmdmap="", size=(16, 2), bufsize=40, curpos=0, scpos=0):
        self.dev = dev
        self.size = size
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
            cmd = chr(rcmd) + ";"
        else:
            cmd = "".join(map(chr, rcmd)) + ";"
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
        self.rpush([self.cmdmap["setCursor"], c, r])
        self.updcur([c, r])

    def print(self, txt):
        self.dev.write((chr(self.cmdmap["print"]) + txt + ";").encode())
        self.updcur(len(txt))
    
    def updcur(self, val, raw=False):
        'flag raw to set instead of displace curpos'
        if type(val) is list:
            val = self.convpos(val)
        if raw:
            self.curpose = val
            return
        else:
            rval = val + self.curpos
            totalbuf = self.bufsize * self.size[1]
            # modding works for both pos and neg val
            self.curpos = rval % totalbuf
        print(self.curpos)
            
    def convpos(self, curpos):
        if type(curpos) is list:
            return curpos[0]  + curpos[1] * self.bufsize
        elif type(curpos) is int:
            return [curpos % self.bufsize, int(curpos / self.bufsize)]
    
            
usb = Serial("COM5")
lcd = Lcd(usb)

sleep(3)
# rcmd = [32, 0, 1]

# lcd.rpush([32, 0, 1])

# usb.write((chr(33) + "World;").encode())

# lcd.rpush(38)
# lcd.rpush(36)
# lcd.rpush(41)

# # usb.write((chr(33) + "123456789abcdefgh;").encode())
# # lcd.rpush(50)

# lcd.rpush([32, 10, 0])

# lcd.rpush(53)
# usb.write((chr(33) + "abc;").encode())
# lcd.rpush(51)
# lcd.rpush(51)
# lcd.setCursor(15, 1)
lcd.push("home")
# lcd.push("autoscroll")
lcd.push("cursor")
# lcd.setCursor(0, 39)
p = "ASCII stands for American Standard Code for Information Interchange."
p = "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
p = "3.141592653589793238462643383279502884193.14159265358979323846264338327950288419"
# p = "3.14159265358979323846264338327950288419"
lcd.print(p)
lcd.setCursor(5, 1)
print(lcd.curpos)
# for i, c in enumerate(p):
#     sleep(.25)
#     lcd.print(c)
        # if i > 14:
        #     lcd.push("scrollDisplayLeft")
    # lcd.push("home")
# while True:
#     sleep(.2)
#     lcd.push("scrollDisplayRight")
# sleep(5)

#lcd.push("clear")
#lcd.setCursor(0, 41)
#lcd.print("x")
# sleep(1) 