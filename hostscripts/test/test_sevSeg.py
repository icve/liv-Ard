import unittest
from lib import SevSeg


class tsDev:
    opt = None

    def write(self, txt):
        self.opt = txt

    def clr(self):
        self.opt = None


class TestSevSeg(unittest.TestCase):

    def setUp(self):
        self.dev = tsDev()
        self.ss = SevSeg(self.dev)
    def tearDown(self):
        self.dev.clr()

    def test_clear(self):
        self.ss.clear()
        self.assertEqual(self.dev.opt, b"00;")

    def test_clear_devid(self):
        self.ss.dev_id = 1
        self.ss.clear()
        self.assertEqual(self.dev.opt, b"01;")

    def test_printrow(self):
        self.ss.printrow("FF")
        self.assertEqual(self.dev.opt, b"r0FF;")

    def test_printcol(self):
        self.ss.printcol("FF")
        self.assertEqual(self.dev.opt, b"c0FF;")

    def test_setled(self):
        self.ss.setled(1,2,1)
        self.assertEqual(self.dev.opt, b"l0121;")

    def test_setstate(self):
        self.ss.setstate(0)
        self.assertEqual(self.dev.opt, b"s00;")

    def test_setintensity(self):
        self.ss.setintensity(15)
        self.assertEqual(self.dev.opt, b"i015;")
