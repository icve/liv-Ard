from .dev4testing import Dev
import unittest
from lib import Lcd

class TestLcd(unittest.TestCase):

    def setUp(self):
        self.dev = Dev(tostr=True)
        self.ss = Lcd(self.dev)

    def tearDown(self):
        self.dev.clr()

    def test_backlight_buffer(self):
       self.ss.backlight(1)
       exp = "x" + chr(34) +";"
       self.assertEqual(self.dev.pop(), exp)

       self.ss.backlight(1)
       self.assertIsNone(self.dev.pop(), exp)

       self.ss.backlight(0)
       exp = "x" + chr(35) +";"
       self.assertEqual(self.dev.pop(), exp)

       self.ss.backlight(0)
       self.assertIsNone(self.dev.pop())

       self.ss.backlight(1)
       exp = "x" + chr(34) +";"
       self.assertEqual(self.dev.pop(), exp)