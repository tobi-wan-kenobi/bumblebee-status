import unittest

import bumblebee.config
import bumblebee.modules.cpu

class FakeOutput(object):
    def add_callback(self, cmd, button, module=None):
        pass

class TestCpuModule(unittest.TestCase):
    def setUp(self):
        output = FakeOutput()
        config = bumblebee.config.Config(["-m", "cpu"])
        self.cpu = bumblebee.modules.cpu.Module(output, config, None)

    def test_documentation(self):
        self.assertTrue(hasattr(bumblebee.modules.cpu, "description"))
        self.assertTrue(hasattr(bumblebee.modules.cpu, "parameters"))

    def test_warning(self):
        self.assertTrue(hasattr(self.cpu, "warning"))

    def test_critical(self):
        self.assertTrue(hasattr(self.cpu, "critical"))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
