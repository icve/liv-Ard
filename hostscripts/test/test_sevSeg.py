import unittest
from lib import SevSeg
from .dev4testing import Dev


def test_dev_id_wrapper(func):

    def wrp_func(self):
        for dev_id in range(10):
            self.ss.dev_id = dev_id
            func(self, dev_id)
    return wrp_func

class TestSevSeg(unittest.TestCase):

    def setUp(self):
        self.dev = Dev()
        self.ss = SevSeg(self.dev)

    def tearDown(self):
        self.dev.clr()

    @test_dev_id_wrapper
    def test_clear(self, dev_id):
        self.ss.clear()
        self.assertEqual(self.dev.pop(), "0{};".format(dev_id).encode())

    def test_clear_devid(self):
        self.ss.dev_id = 1
        self.ss.clear()
        self.assertEqual(self.dev.pop(), b"01;")

    def test_printrow(self):
        self.ss.printrow("FF")
        self.assertEqual(self.dev.pop(), b"r0FF;")

    def test_printcol(self):
        self.ss.printcol("FF")
        self.assertEqual(self.dev.pop(), b"c0FF;")

    def test_setled(self):
        self.ss.setled(1,2,1)
        self.assertEqual(self.dev.pop(), b"l0121;")

    def test_setstate(self):
        self.ss.setstate(0)
        self.assertEqual(self.dev.pop(), b"s00;")

    def test_setintensity(self):
        self.ss.setintensity(15)
        self.assertEqual(self.dev.pop(), b"i015;")

    def test_write_one_char(self):
        self.ss.write("-", 1, 1)
        self.assertEqual(self.dev.pop(), b"a01-1;")

    def test_onstate_buffer(self):
        self.ss.setstate(0)
        self.assertEqual(self.dev.pop(), b"s00;")
        self.ss.setstate(0)
        self.assertIsNone(self.dev.pop())

        self.ss.setstate(1)
        self.assertEqual(self.dev.pop(), b"s01;")
        self.ss.setstate(1)
        self.assertIsNone(self.dev.pop())


