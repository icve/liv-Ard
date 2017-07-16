from random import randrange

MTXSIZE = 8


class Rainfall:
    def __init__(self, mtxdev, maxstroke=4, height=3, speed=2):
        self.dev = mtxdev
        self.height = height
        self.maxstroke = maxstroke
        self.speed = speed
        self.strokes = []

    def add_random_strokes(self):
        while len(self.strokes) < self.maxstroke:
            s = _Stroke(randrange(MTXSIZE))
            if s not in self.strokes:
                self.strokes.append(s)

    def update(self):
        self.add_random_strokes()
        for s in self.strokes:
            pl = hex(s.b_value).replace("0x", "")
            self.dev.printcol(s.pos, pl)
            if s.phase < s.height:
                s.b_value = (s.b_value << 1) + 1
            elif s.phase >= MTXSIZE:
                s.b_value = s.b_value - (1 << s.phase - s.height)
            else:
                s.b_value = s.b_value << 1

            s.phase += 1
            if s.b_value == 0:
                self.strokes.remove(s)


class _Stroke:
    def __init__(self, pos, phase=0, height=3):
        self.pos = pos
        self.phase = phase
        self.height = height
        self.b_value = 0

    def __eq__(self, o):
        return self.pos == o.pos
