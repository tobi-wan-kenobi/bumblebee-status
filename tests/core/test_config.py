import os
import unittest

import core.config


class config(unittest.TestCase):
    def setUp(self):
        self.someModules = ["b", "x", "a"]
        self.moreModules = ["this", "module", "here"]
        self.someTheme = "some-theme"
        self.someIconset = "some-iconset"
        self.defaultConfig = core.config.Config([])

    def test_module(self):
        cfg = core.config.Config(["-m"] + self.someModules)
        self.assertEqual(self.someModules, cfg.modules())

    def test_module_ordering_maintained(self):
        cfg = core.config.Config(["-m"] + self.someModules + ["-m"] + self.moreModules)
        self.assertEqual(self.someModules + self.moreModules, cfg.modules())

    def test_default_interval(self):
        self.assertEqual(1, self.defaultConfig.interval())

    def test_interval(self):
        cfg = core.config.Config(["-p", "interval=4"])
        self.assertEqual(4, cfg.interval())

    def test_float_interval(self):
        cfg = core.config.Config(["-p", "interval=0.5"])
        self.assertEqual(0.5, cfg.interval())

    def test_default_theme(self):
        self.assertEqual("default", self.defaultConfig.theme())

    def test_theme(self):
        cfg = core.config.Config(["-t", self.someTheme])
        self.assertEqual(self.someTheme, cfg.theme())

    def test_default_iconset(self):
        self.assertEqual("auto", self.defaultConfig.iconset())

    def test_iconset(self):
        cfg = core.config.Config(["-i", self.someIconset])
        self.assertEqual(self.someIconset, cfg.iconset())

    def test_right_to_left(self):
        cfg = core.config.Config(["-r"])
        self.assertTrue(cfg.reverse())
        self.assertFalse(self.defaultConfig.reverse())

    def test_logfile(self):
        cfg = core.config.Config(["-f", "my-custom-logfile"])
        self.assertEqual(None, self.defaultConfig.logfile())
        self.assertEqual("my-custom-logfile", cfg.logfile())

    def test_all_modules(self):
        modules = core.config.all_modules()
        self.assertGreater(len(modules), 0)
        for module in modules:
            pyname = "{}.py".format(module)
            base = os.path.abspath(
                os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..",
                    "..",
                    "bumblebee_status",
                    "modules",
                )
            )
            self.assertTrue(
                os.path.exists(os.path.join(base, "contrib", pyname))
                or os.path.exists(os.path.join(base, "core", pyname))
            )

    def test_list_output(self):
        with unittest.mock.patch("core.config.sys") as sys:
            cfg = core.config.Config(["-l", "themes"])
            cfg = core.config.Config(["-l", "modules"])
            cfg = core.config.Config(["-l", "modules-rst"])
            # TODO: think of some plausibility testing here

    def test_missing_parameter(self):
        cfg = core.config.Config(["-p", "test.key"])
        self.assertEqual("no-value-set", cfg.get("test.key", "no-value-set"))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
