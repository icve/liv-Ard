import unittest
from lib.sevSeg import SevSeg
from .dev4testing import Dev


def test_dev_id_wrapper(func):

    def wrp_func(self):
        for dev_id in range(10):
            self.ss.dev_id = dev_id
            func(self, dev_id)
    return wrp_func


def bc(c):
    return chr(c).encode()


class TestSevSeg(unittest.TestCase):

    def setUp(self):
        self.dev = Dev()
        self.ss = SevSeg(self.dev)

    def tearDown(self):
        self.dev.clr()

    @test_dev_id_wrapper
    def test_clear(self, dev_id):
        self.ss.clear()
        rlt = "{}{};".format(chr(84), dev_id).encode()
        self.assertEqual(self.dev.pop(), rlt)

    def test_clear_devid(self):
        self.ss.dev_id = 1
        self.ss.clear()
        self.assertEqual(self.dev.pop(), bc(84) + b"1;")

    def test_printrow(self):
        self.ss.printrow(1, "F")
        self.assertEqual(self.dev.pop(), bc(79) + b"01F;")

    def test_printcol(self):
        self.ss.printcol(0, "F")
        self.assertEqual(self.dev.pop(), bc(80) + b"00F;")

    def test_setled(self):
        self.ss.setled(1,2,1)
        self.assertEqual(self.dev.pop(), bc(81) + b"0121;")

    def test_setstate(self):
        self.ss.setstate(0)
        self.assertEqual(self.dev.pop(), bc(82) + b"00;")

    def test_setintensity(self):
        self.ss.setintensity(15)
        self.assertEqual(self.dev.pop(), bc(83) + b"015;")
    
    def test_write_one_char(self):
        self.ss.write("-", 1, 1)
        self.assertEqual(self.dev.pop(), bc(77) + b"01-1;")

    def test_onstate_buffer(self):
        self.ss.setstate(0)
        self.assertEqual(self.dev.pop(), bc(82) + b"00;")
        self.ss.setstate(0)
        self.assertIsNone(self.dev.pop())

        self.ss.setstate(1)
        self.assertEqual(self.dev.pop(), bc(82) + b"01;")
        self.ss.setstate(1)
        self.assertIsNone(self.dev.pop())


