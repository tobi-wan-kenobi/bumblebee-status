import unittest

import core.decorators
import core.widget
import core.module
import core.config


class TestModule(core.module.Module):
    def __init__(self, config=None, theme=None):
        config = core.config.Config([])
        super().__init__(config, theme, core.widget.Widget(self.get))
        self.text = ""

    @core.decorators.scrollable
    def get(self, widget):
        return self.text


class config(unittest.TestCase):
    def setUp(self):
        self.module = TestModule()
        self.widget = self.module.widget()
        self.width = 10
        self.module.set("width", self.width)

    def test_no_text(self):
        self.assertEqual("", self.module.text)
        self.assertEqual("", self.module.get(self.widget))

    def test_smaller(self):
        self.module.text = "test"
        self.assertLess(len(self.module.text), self.width)
        self.assertEqual("test", self.module.get(self.widget))

    def test_bigger(self):
        self.module.text = "abcdefghijklmnopqrst"
        self.assertGreater(len(self.module.text), self.width)
        self.assertEqual(self.module.text[: self.width], self.module.get(self.widget))

    def test_bounce(self):
        self.module.text = "abcd"
        self.module.set("width", 2)
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("ab", self.module.get(self.widget))

    def test_nobounce(self):
        self.module.set("scrolling.bounce", False)
        self.module.text = "abcd"
        self.module.set("width", 2)
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
