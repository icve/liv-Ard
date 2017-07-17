from random import randrange, uniform
from time import time

MTXSIZE = 8

# TODO move MTXSIZE
# TODO reverse fall toggle
# TODO over size stroke
# TODO wirte test file


class Rainfall:
    def __init__(self, mtxdev,
                 maxstroke=4,
                 max_height=4,
                 min_height=1,
                 max_speed=4,
                 min_speed=1,
                 down=True):
        self.dev = mtxdev
        self.max_height = max_height
        self.min_height = min_height
        self.maxstroke = maxstroke
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.strokes = []
        self.down = down

    def add_random_strokes(self):
        while len(self.strokes) < self.maxstroke:
            h = randrange(self.min_height, self.max_height)
            sp = uniform(self.min_speed, self.max_speed)
            s = _Stroke(randrange(MTXSIZE), height=h, speed=sp)
            if s not in self.strokes:
                self.strokes.append(s)

    def update(self):
        self.add_random_strokes()
        for s in self.strokes:
            s.update()
            pl = hex(s.b_value).replace("0x", "")
            self.dev.printcol(s.pos, pl)
            if s.b_value == 0:
                self.strokes.remove(s)


class _Stroke:
    def __init__(self, pos, phase=0, height=3, speed=2):
        self.pos = pos
        self.phase = phase
        self.height = height
        self.b_value = 0
        self.update_every = 1 / speed
        self.last_update = time() - self.update_every - 1
        # for test injection
        self.time = time

    def update(self):
        t = self.time()
        if t - self.last_update > self.update_every:
            if self.phase < self.height:
                self.b_value = (self.b_value << 1) + 1
            elif self.phase >= MTXSIZE:
                self.b_value = self.b_value - (1 << self.phase - self.height)
            else:
                self.b_value = self.b_value << 1
            self.phase += 1
            self.last_update = t

    def __eq__(self, o):
        return self.pos == o.pos
