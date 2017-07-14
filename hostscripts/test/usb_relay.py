
# relay for debug

class Usb_relay:
    def __init__(self, usb):
        self.usb = usb
    def read(self, i):
        print("read")
        return self.usb.read(i)
    def write(self, s):
        print(s.decode().split())
        self.usb.write(s)
