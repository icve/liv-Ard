from random import randrange, uniform
from time import time

MTXSIZE = 8

# TODO move MTXSIZE
# TODO over size stroke
# TODO wirte test file
# TODO randomise up_down


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
            s = _Stroke(randrange(MTXSIZE), height=h, speed=sp, down=self.down)
            if s not in self.strokes:
                self.strokes.append(s)

    def update(self):
        self.add_random_strokes()
        for s in self.strokes:
            if s.update():
                pl = hex(s.b_value).replace("0x", "")
                self.dev.printcol(s.pos, pl)
                if s.b_value == 0:
                    self.strokes.remove(s)


class _Stroke:
    def __init__(self, pos, height=3, speed=2, down=True, phase=0):
        self.pos = pos
        self.phase = phase
        self.height = height
        self.b_value = 0
        self.update_every = 1 / speed
        self.down = down
        self.last_update = time() - self.update_every - 1
        # for test injection
        self.time = time

    def update(self):
        """ return false if not updated"""
        t = self.time()
        if (t - self.last_update) > self.update_every:
            if self.down:
                self.fall_down()
            else:
                self.fall_up()
            self.phase += 1
            self.last_update = t
            return True
        return False

    def fall_up(self):
        if self.phase < self.height:
            self.b_value = (self.b_value << 1) + 1
        # elif self.phase >= MTXSIZE:
        #    self.b_value = self.b_value - (1 << self.phase - self.height)
        else:
            # mask byte to keep value from exceeding limit
            self.b_value = (self.b_value << 1) & 0xFF

    def fall_down(self):
        if self.phase < self.height:
            self.b_value = (self.b_value >> 1) + 0x80
        else:
            self.b_value = self.b_value >> 1

    def __eq__(self, o):
        return self.pos == o.pos
