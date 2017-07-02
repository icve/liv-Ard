
class Dev:

    def __init__(self, tostr=False):
        self.opt = []
        self.tostr = tostr

    def write(self, txt):
        self.opt.append(txt)

    def clr(self):
        self.opt = []

    def pop(self):
        if not self.opt:
            return None

        if self.tostr:
            return self.opt.pop().decode()
        else:
            return self.opt.pop()
