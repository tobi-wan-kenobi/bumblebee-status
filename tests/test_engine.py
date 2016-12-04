# pylint: disable=C0103,C0111
import unittest

from bumblebee.engine import Engine

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(None)

    def test_stop(self):
        self.assertTrue(self.engine.running())
        self.engine.stop()
        self.assertFalse(self.engine.running())
