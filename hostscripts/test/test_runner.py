import unittest
from lib.runner import Runner


class Test_runner(unittest.TestCase):

    def setUp(self):
        self.r = Runner()

    def test_update(self):
        c1 = [0]
        c2 = [0]
        class M:
            def __init__(self,c):
                self.c = c
            def update(self):
                self.c[0] += 1
        self.r.add_module(M(c1))
        self.r.add_module(M(c2))
        self.r.update()
        self.assertEqual(c1[0], 1)
        self.assertEqual(c2[0], 1)
