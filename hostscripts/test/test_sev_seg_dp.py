import unittest
from lib.sev_seg_dp import Sev_seg_dp
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
        self.ss = Sev_seg_dp(self.dev)

    def tearDown(self):
        self.dev.clr()

    @test_dev_id_wrapper
    def test_clear(self, dev_id):
        self.ss.clear()
        rlt = "{}{};".format(chr(84), chr(dev_id)).encode()
        self.assertEqual(self.dev.pop(), rlt)

    def test_clear_devid(self):
        self.ss.dev_id = 1
        self.ss.clear()
        self.assertEqual(self.dev.pop(), bc(84) + b"\x01;")

    def test_printrow(self):
        self.ss.printrow(1, 0x0F)
        self.assertEqual(self.dev.pop(), bc(79) + b"\x00\x01\x0F;")

    def test_printcol(self):
        self.ss.printcol(0, 0x0F)
        self.assertEqual(self.dev.pop(), bc(80) + b"\x00\x00\x0F;")

    def test_setled(self):
        self.ss.setled(1, 2, 1)
        self.assertEqual(self.dev.pop(), bc(81) + b"\x00\x01\x02\x01;")

    def test_shutdown(self):
        self.ss.shutdown(0)
        self.assertEqual(self.dev.pop(), bc(82) + b"\x00\x00;")

    def test_setintensity(self):
        self.ss.setintensity(15)
        self.assertEqual(self.dev.pop(), bc(83) + b"\x00\x0F;")
    
    def test_write_one_char(self):
        self.ss.write("-", 1, 1)
        self.assertEqual(self.dev.pop(), bc(77) + b"\x00\x01-\x01;")

    def test_shutdown_buffer(self):
        self.ss.shutdown(0)
        self.assertEqual(self.dev.pop(), bc(82) + b"\x00\x00;")
        self.ss.shutdown(0)
        self.assertIsNone(self.dev.pop())

        self.ss.shutdown(1)
        self.assertEqual(self.dev.pop(), bc(82) + b"\x00\x01;")
        self.ss.shutdown(1)
        self.assertIsNone(self.dev.pop())


