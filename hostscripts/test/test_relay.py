import unittest
from lib.relay import Relay
from .dev4testing import Dev


class Test_relay(unittest.TestCase):

    def setUp(self):
        self.dev = Dev()
        self.relay = Relay(self.dev)

    def test_on(self):
        self.relay.on()
        self.assertEqual(self.dev.pop(), bytes((85,)) + b'\x01;')

    def test_off(self):
        self.relay.off()
        self.assertEqual(self.dev.pop(), bytes((85,)) + b'\x00;')

    def test_state(self):
        self.relay.off()
        self.relay.off()
        self.assertEqual(self.dev.pop(), bytes((85,)) + b'\x00;')
        self.assertIsNone(self.dev.pop())
        # off to on
        self.relay.on()
        self.relay.on()
        self.assertEqual(self.dev.pop(), bytes((85,)) + b'\x01;')
        self.assertIsNone(self.dev.pop())
        # on to off
        self.relay.off()
        self.relay.off()
        self.assertEqual(self.dev.pop(), bytes((85,)) + b'\x00;')
        self.assertIsNone(self.dev.pop())

