
class Dev:

    def __init__(self, tostr=False):
        self.opt = []
        self.inp = []
        self.tostr = tostr

    def write(self, txt):
        self.opt.append(txt)

    def read(self, i):
        """ i is ignored """
        return self.inp.pop()

    def clr(self):
        self.opt = []
        self.inp = []

    def pop(self):
        if not self.opt:
            return None

        if self.tostr:
            return self.opt.pop().decode()
        else:
            return self.opt.pop()


""" helper functions"""
# to byte
tb = lambda s: s.encode()
# to string
ts = lambda s: s.decode()
