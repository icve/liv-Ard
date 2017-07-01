def getRing(side=8, ring=0):
    opp_edge = side - 1 - ring
    seqgen = range(side)
    coors = [(str(ring), str(x)) for x in seqgen] +\
        [(str(x), str(opp_edge)) for x in seqgen[1:]] +\
        [(str(opp_edge), str(x)) for x in reversed(seqgen[:-1])] +\
        [(str(x), str(ring)) for x in reversed(seqgen[1:-1])]
    return coors

class ledClockPointer(object):
    def __init__(self, pointertype="sec", siz=1, ring=0):
        self.pt = pointertype
        self.siz = siz
        self.ledRing = getRing(ring=ring)
