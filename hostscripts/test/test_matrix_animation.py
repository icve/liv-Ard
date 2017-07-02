import unittest
from animations import Led_clock_pointer, Linear_display
from .dev4testing import Dev
from lib import SevSeg
from time import strftime


coods = [(0, i) for i in range(30)]


class test_Linear_display(unittest.TestCase):

    def test_get_dot(self):
        ldp = Linear_display(coods=coods)
        self.assertEqual(ldp.get_dot(0), (0, 0))
        self.assertEqual(ldp.get_dot(1), (0, 29))
        self.assertEqual(ldp.get_dot(.5), (0, 14))

    def test_get_dot_displace(self):
        ldp = Linear_display(coods=coods, dsp=5)
        self.assertEqual(ldp.get_dot(0), (0, 5))
        self.assertEqual(ldp.get_dot(1), (0, 4))
        self.assertEqual(ldp.get_dot(.5), (0, 19))
        ldp.dsp = -5
        self.assertEqual(ldp.get_dot(0), (0, 25))
        self.assertEqual(ldp.get_dot(1), (0, 24))
        self.assertEqual(ldp.get_dot(.5), (0, 9))


class test_Led_clock_pointer(unittest.TestCase):

    def test_point_generator(self):
        lcp = Led_clock_pointer(None)
        self.assertAlmostEqual(lcp.point_generator(), int(strftime("%S")) / 59)
        lcp = Led_clock_pointer(None, pointertype="min")
        self.assertAlmostEqual(lcp.point_generator(), int(strftime("%M")) / 59)
        lcp = Led_clock_pointer(None, pointertype="hour")
        self.assertAlmostEqual(lcp.point_generator(), int(strftime("%H")) / 23)

    def test_update(self):
        dev = Dev(True)
        ss = SevSeg(dev)
        lcp = Led_clock_pointer(ss)
        lcp.point_generator = lambda: 0
        lcp.update()
        self.assertEqual(dev.pop(), "l0041;")
        self.assertEqual(dev.pop(), "00;")
        lcp.update()
        self.assertIsNone(dev.pop())

        lcp.point_generator = lambda: 1
        lcp.update()
        self.assertEqual(dev.pop(), "l0031;")

        lcp.point_generator = lambda: .5
        lcp.update()
        self.assertEqual(dev.pop(), "l0741;")
