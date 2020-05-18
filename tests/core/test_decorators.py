import unittest

import core.decorators
import core.widget
import core.module
import core.config


class TestModule(core.module.Module):
    @core.decorators.never
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
        self.module.set("scrolling.width", self.width)

    def test_never(self):
        self.module = TestModule()
        self.assertEqual("never", self.module.parameter("interval"))

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
        self.module.set("scrolling.width", 2)
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
        self.module.set("scrolling.width", 2)
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.assertEqual("cd", self.module.get(self.widget))

    def test_changed_data(self):
        self.module.text = "abcd"
        self.module.set("scrolling.width", 2)
        self.assertEqual("ab", self.module.get(self.widget))
        self.assertEqual("bc", self.module.get(self.widget))
        self.module.text = "wxyz"
        self.assertEqual("wx", self.module.get(self.widget))

    def test_minimum_changed_data(self):
        self.module.text = "this is a sample song (0:00)"
        self.module.set("scrolling.width", 10)
        self.assertEqual(self.module.text[0:10], self.module.get(self.widget))
        self.module.text = "this is a sample song (0:01)"
        self.assertEqual(self.module.text[1:11], self.module.get(self.widget))
        self.module.text = "this is a sample song (0:12)"
        self.assertEqual(self.module.text[2:12], self.module.get(self.widget))
        self.module.text = "this is a different song (0:12)"
        self.assertEqual(self.module.text[0:10], self.module.get(self.widget))

    def test_n_plus_one(self):
        self.module.text = "10 letters"
        self.module.set("scrolling.width", 9)
        self.assertEqual(self.module.text[0:9], self.module.get(self.widget))
        self.assertEqual(self.module.text[1:10], self.module.get(self.widget))
        self.assertEqual(self.module.text[0:9], self.module.get(self.widget))
        self.assertEqual(self.module.text[1:10], self.module.get(self.widget))
        self.assertEqual(self.module.text[0:9], self.module.get(self.widget))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
