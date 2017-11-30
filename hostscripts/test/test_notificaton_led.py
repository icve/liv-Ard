import unittest
from lib.notification_led import Notification_led
from .dev4testing import Dev, tb

LEDCHAR = chr(75)
class TestNotification_led(unittest.TestCase):
    def setUp(self):
        self.dev = Dev()
        self.led = Notification_led(self.dev)

    def test_set_led(self):
        self.led.set_led(1)
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x01;"))

        # buffer
        self.led.set_led(1)
        self.assertIsNone(self.dev.pop())

        self.led.set_led(0)
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x00;"))
