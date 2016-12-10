# pylint: disable=C0103,C0111

import json
import unittest
import mock

import bumblebee.input
from bumblebee.input import I3BarInput
from bumblebee.modules.caffeine import Module
from tests.util import MockEngine, MockConfig, assertPopen

class TestCaffeineModule(unittest.TestCase):
    def setUp(self):
        self.engine = MockEngine()
        self.engine.input = I3BarInput()
        self.engine.input.need_event = True
        self.engine.input.need_valid_event = True
        self.config = MockConfig()
        self.module = Module(engine=self.engine, config={ "config": self.config })
        for widget in self.module.widgets():
            widget.link_module(self.module)
