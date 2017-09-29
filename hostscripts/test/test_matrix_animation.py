import unittest
from animations.matrix_animation import Led_clock_pointer, Linear_display, _get_ring
from .dev4testing import Dev
from lib.sevSeg import SevSeg
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
        self.assertEqual(dev.pop(), chr(81) + "0041;")
        self.assertIsNone(dev.pop())

        # check clear queue
        self.assertEqual(len(lcp.off_queue), 27)
        lcp.update()
        self.assertEqual(dev.pop(), chr(81) + "0050;")
        self.assertEqual(len(lcp.off_queue), 26)
        for _ in range(27):
            lcp.update()
            dev.pop()

        lcp.update()
        self.assertEqual(len(lcp.off_queue), 0)
        self.assertIsNone(dev.pop())

        lcp.point_generator = lambda: 1
        lcp.update()
        self.assertEqual(dev.pop(), chr(81) + "0031;")

        lcp.point_generator = lambda: .5
        lcp.update()
        self.assertEqual(dev.pop(), chr(81) + "0741;")


class test_get_ring(unittest.TestCase):

    def test_get_ring(self):
        # currently only testing for the number of led cood to be generated
        self.assertEqual(len(_get_ring(ring=0)), 28)
        self.assertEqual(len(_get_ring(ring=1)), 20)
        self.assertEqual(len(_get_ring(ring=2)), 12)
        self.assertEqual(len(_get_ring(ring=3)), 4)
