from time import localtime


def _get_ring(side=8, ring=0):
    seqgen = range(ring, side - ring)
    coors = [(ring, x) for x in seqgen] +\
        [(x, seqgen[-1]) for x in seqgen[1:]] +\
        [(seqgen[-1], x) for x in reversed(seqgen[:-1])] +\
        [(x, ring) for x in reversed(seqgen[1:-1])]
    return coors


class Led_clock_pointer(object):
    def __init__(self, mtxdev, pointertype="sec", ring=0, dsp=None):
        self.pt = pointertype
        dsp = dsp if dsp else int(4 - ring)
        self.linear_display = Linear_display(_get_ring(ring=ring), dsp)
        self.mtxdev = mtxdev
        self.point_generator = {
                "sec": lambda: localtime().tm_sec / 59,
                "min": lambda: localtime().tm_min / 59,
                "hour": lambda: localtime().tm_hour / 23
                }[pointertype]
        self.lastcood = None
        self.off_queue = []

    def update(self):
        """ this method 'renders' a frame"""
        # handle queue before jumping out
        if self.off_queue:
            self.mtxdev.setled(*self.off_queue.pop(), 0)

        n = self.point_generator()
        cood = self.linear_display.get_dot(n)
        if cood == self.lastcood:
            return

        if n == 0:
            # self.mtxdev.clear()
            # clear Linear display slowly
            self.off_queue += reversed(self.linear_display.get_coods()[1:])
        self.mtxdev.setled(*cood, 1)
        self.lastcood = cood


class Led_clock_flasher:
    def __init__(self, mtxdev, coods=None, speed=1):
        self.mtxdev = mtxdev
        self.speed = speed
        # default to the inner 4 dots
        self.coods = coods if coods else _get_ring(ring=3)
        self.state = None
        self.state_generator = lambda: int(localtime().tm_sec * speed) % 2

    def update(self):
        new_state = self.state_generator()
        if new_state != self.state:
            self.set_state(new_state)
            self.state = new_state

    def set_state(self, on):
        """turn on/off all led in coods by flagging 1/0"""
        for cood in self.coods:
            self.mtxdev.setled(*cood, on)


class Linear_display:
    def __init__(self, coods, dsp=0):
        self.coods = coods
        self.dsp = dsp

    def get_idx(self, n):
        """get index base on percentage(0 - 1)"""
        clen = len(self.coods)
        idx = int(n * (clen - 1)) + self.dsp
        safeidx = idx % clen
        return safeidx

    def get_dot(self, n):
        """ get cood of dot base on percentage(0 - 1)"""
        return self.coods[self.get_idx(n)]

    def get_line(self, n):
        """get list of cood base on percentage(0 - 1)"""
        return self.coods[:self.get_idx(n)]

    def get_coods(self, use_dsp=True):
        """ get content of coods, flag to enable displacing items"""
        if not use_dsp or self.dsp == 0:
            return self.coods
        return self.coods[self.dsp:] + self.coods[:self.dsp]
