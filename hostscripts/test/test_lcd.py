from .dev4testing import Dev
import unittest
from lib.lcdControl import Lcd




class TestLcd(unittest.TestCase):

    def setUp(self):
        self.dev = Dev(tostr=True)
        self.ss = Lcd(self.dev)

    def tearDown(self):
        self.dev.clr()

    def test_backlight_buffer(self):
        self.ss.backlight(1)
        exp = "x" + chr(34) + ";"
        self.assertEqual(self.dev.pop(), exp)

        self.ss.backlight(1)
        self.assertIsNone(self.dev.pop(), exp)

        self.ss.backlight(0)
        exp = "x" + chr(35) + ";"
        self.assertEqual(self.dev.pop(), exp)

        self.ss.backlight(0)
        self.assertIsNone(self.dev.pop())

        self.ss.backlight(1)
        exp = "x" + chr(34) + ";"
        self.assertEqual(self.dev.pop(), exp)

    def test_clear(self):
        self.ss.clear()
        exp = "x" + chr(40) + ";"
        self.assertEqual(self.dev.pop(), exp)

        # testing clear buffer
        # regexp matching may be better suited

        # mathing with set
        self.ss.buf[0][0] = "s"
        self.assertEqual(set(str(self.ss.buf)), set(r"['s, ]"))
        self.ss.clear()
        self.assertEqual(set(str(self.ss.buf)), set(r"[' ,]"))
        self.dev.clr()

        # test cursor pos
        self.ss.curpos = 1
        self.ss.clear()
        self.assertEqual(self.ss.curpos, 0)
        self.dev.clr()
