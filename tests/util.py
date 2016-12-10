# pylint: disable=C0103,C0111,W0613

import shlex
import subprocess

from bumblebee.output import Widget

def assertWidgetAttributes(test, widget):
    test.assertTrue(isinstance(widget, Widget))
    test.assertTrue(hasattr(widget, "full_text"))

def assertPopen(output, cmd):
    res = shlex.split(cmd)
    output.assert_called_with(res,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

class MockInput(object):
    def start(self):
        pass

    def stop(self):
        pass

    def register_callback(self, obj, button, cmd):
        pass

class MockEngine(object):
    def __init__(self):
        self.input = MockInput()

class MockConfig(object):
    def __init__(self):
        self._data = {}

    def get(self, name, default):
        if name in self._data:
            return self._data[name]
        return default

    def set(self, name, value):
        self._data[name] = value

class MockOutput(object):
    def start(self):
        pass

    def stop(self):
        pass

    def draw(self, widget, engine, module):
        engine.stop()

    def begin(self):
        pass

    def flush(self):
        pass

    def end(self):
        pass

class MockModule(object):
    def __init__(self, engine=None, config=None):
        self.id = None

class MockWidget(Widget):
    def __init__(self, text):
        super(MockWidget, self).__init__(text)
        self._text = text
        self.module = None
        self.attr_state = ["state-default"]
        self.id = "none"

    def state(self):
        return self.attr_state

    def update(self, widgets):
        pass

    def full_text(self):
        return self._text

class MockTheme(object):
    def __init__(self):
        self.attr_prefix = None
        self.attr_suffix = None
        self.attr_fg = None
        self.attr_bg = None
        self.attr_separator = None
        self.attr_separator_block_width = 0

    def padding(self, widget):
        return ""

    def reset(self):
        pass

    def separator_block_width(self, widget):
        return self.attr_separator_block_width

    def separator(self, widget):
        return self.attr_separator

    def prefix(self, widget, default=None):
        return self.attr_prefix

    def suffix(self, widget, default=None):
        return self.attr_suffix

    def fg(self, widget):
        return self.attr_fg

    def bg(self, widget):
        return self.attr_bg

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
