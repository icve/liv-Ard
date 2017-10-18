from .dev4testing import Dev, tb
import unittest
from lib.motion_sensor import Motion_sensor
from tempfile import NamedTemporaryFile
from time import sleep

POLLCHAR = chr(76).encode()
LEDCHAR = chr(75)

class TestMotionSensor(unittest.TestCase):
    def setUp(self):
        self.dev = Dev()
        self.tempfile = NamedTemporaryFile(mode='r')
        self.ms = Motion_sensor(self.dev, self.tempfile.name)

    def tearDown(self):
        self.tempfile.close()

    def test_init(self):
        self.assertIn("Starting", self.tempfile.file.read())

    def test_get_state(self):
        self.dev.inp.append(b'\x00')
        self.assertEqual(self.ms.get_state(), 0)
        self.assertEqual(self.dev.pop(), POLLCHAR + b";")

        self.assertIsNone(self.dev.pop())
        self.assertEqual(self.dev.inp, [])

        self.dev.inp.append(b'\x01')
        self.assertEqual(self.ms.get_state(), 1)

    def test_set_led(self):
        self.ms.set_led(1)
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x01;"))

        # buffer
        self.ms.set_led(1)
        self.assertIsNone(self.dev.pop())

        self.ms.set_led(0)
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x00;"))

    def test_update(self):
        # first update
        self.ms.get_time = lambda: 0
        self.dev.inp.append(b'\x00')
        self.ms.update()
        self.tempfile.file.readline()
        ptn = r"(\d{2}/){2}\d{2} (\d{2}:){2}\d{2}, 0\s"
        self.assertRegex(self.tempfile.file.read(), ptn)
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x00;"))
        self.assertEqual(self.dev.pop(), POLLCHAR + b";")
        # before timeout
        self.ms.update()
        self.assertEqual(self.tempfile.file.read(), "")
        self.assertIsNone(self.dev.pop())
        # timeout no state update
        self.ms.get_time = lambda: 2
        self.dev.inp.append(b'\x00')
        self.ms.update()
        self.assertEqual(self.dev.pop(), POLLCHAR + b";")
        self.assertEqual(self.tempfile.file.read(), "")
        # timeout with state update
        self.ms.get_time = lambda: 4
        self.dev.inp.append(b'\x01')
        self.ms.update()
        self.assertEqual(self.dev.pop(), tb(LEDCHAR + "\x01;"))
        self.assertEqual(self.dev.pop(), POLLCHAR + b";")
        self.assertRegex(self.tempfile.file.read(), ptn.replace("0", "1"))
