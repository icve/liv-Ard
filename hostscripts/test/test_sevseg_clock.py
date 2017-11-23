from animations.seven_segment_clock import Seven_segment_clock
from test.dev4testing import Dev
from datetime import datetime
from lib.sevSeg import SevSeg
import unittest

fromtimestamp = datetime.utcfromtimestamp

dev = Dev()
ss = SevSeg(dev)

class TestSevenSegmentClock(unittest.TestCase):

    def setUp(self):
        dev.clr()
    def test_update(self):
        c = Seven_segment_clock(ss)
        c.get_time = lambda: 0
        c.strftime = fromtimestamp(0).strftime
        c.update()

        STR = "00-00-00"
        for i in range(7, -1, -1):
            self.assertEqual(dev.pop(), bytes([77, 0, i, ord(STR[i]), 0, ord(';')]))
        
        c.update()
        self.assertIsNone(dev.pop())

        c.get_time = lambda: 2
        c.strftime = fromtimestamp(1).strftime
        c.update()
        self.assertIsNotNone(dev.pop())

