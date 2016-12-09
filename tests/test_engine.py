# pylint: disable=C0103,C0111,W0703

import unittest

from bumblebee.error import ModuleLoadError
from bumblebee.engine import Engine
from bumblebee.config import Config

from tests.util import MockOutput

class TestEngine(unittest.TestCase):
    def setUp(self):
        self.engine = Engine(config=Config(), output=MockOutput())
        self.singleWidgetModule = [{"module": "test", "name": "a"}]
        self.testModule = "test"
        self.invalidModule = "no-such-module"
        self.testModuleSpec = "bumblebee.modules.{}".format(self.testModule)
        self.testModules = [
            {"module": "test", "name": "a"},
            {"module": "test", "name": "b"},
        ]

    def test_stop(self):
        self.assertTrue(self.engine.running())
        self.engine.stop()
        self.assertFalse(self.engine.running())

    def test_load_module(self):
        module = self.engine.load_module(self.testModule)
        self.assertEquals(module.__module__, self.testModuleSpec)

    def test_load_invalid_module(self):
        with self.assertRaises(ModuleLoadError):
            self.engine.load_module(self.invalidModule)

    def test_load_none(self):
        with self.assertRaises(ModuleLoadError):
            self.engine.load_module(None)

    def test_load_modules(self):
        modules = self.engine.load_modules(self.testModules)
        self.assertEquals(len(modules), len(self.testModules))
        self.assertEquals(
            [module.__module__ for module in modules],
            [self.testModuleSpec for module in modules]
        )

    def test_run(self):
        self.engine.load_modules(self.singleWidgetModule)
        try:
            self.engine.run()
        except Exception as e:
            self.fail(e)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
