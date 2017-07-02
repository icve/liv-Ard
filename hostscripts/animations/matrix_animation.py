from time import time


def get_ring(side=8, ring=0):
    opp_edge = side - 1 - ring
    seqgen = range(side)
    coors = [(str(ring), str(x)) for x in seqgen] +\
        [(str(x), str(opp_edge)) for x in seqgen[1:]] +\
        [(str(opp_edge), str(x)) for x in reversed(seqgen[:-1])] +\
        [(str(x), str(ring)) for x in reversed(seqgen[1:-1])]
    return coors


class Led_clock_pointer(object):
    def __init__(self, mtxdev, pointertype="sec", ring=0, dsp=4):
        self.pt = pointertype
        self.linear_display = Linear_display(get_ring(ring=ring), dsp)
        self.mtxdev = mtxdev
        self.point_generator = {
                "sec": lambda: int(time()) % 60 / 59,
                "min": lambda: int(time()) / 60 % 60 / 59,
                "hour": lambda: int(time()) / 3600 % 24 / 23
                }[pointertype]
        self.lastcood = None

    def update(self):
        n = self.point_generator()
        cood = self.linear_display.get_dot(n)
        if cood == self.lastcood:
            return

        if n == 0:
            self.mtxdev.clear()
        self.mtxdev.setled(cood[0], cood[1], 1)
        self.lastcood = cood


class Linear_display:
    def __init__(self, coods, dsp=0):
        self.coods = coods
        self.dsp = dsp

    def get_dot(self, n):
        """ get cood of dot base on percentage(0 - 1)"""
        clen = len(self.coods)
        idx = int(n * (clen - 1)) + self.dsp
        safeidx = idx % clen
        return self.coods[safeidx]
