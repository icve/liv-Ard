
class Dev:

    def __init__(self, tostr=False):
        self.opt = None
        self.tostr = tostr

    def write(self, txt):
        self.opt = txt

    def clr(self):
        self.opt = None

    def pop(self):
        if self.opt is None:
            return None

        rlt = self.opt
        self.clr()
        if self.tostr:
            return rlt.decode()
        else:
            return rlt

