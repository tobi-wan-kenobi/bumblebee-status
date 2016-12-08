# pylint: disable=C0103,C0111,W0613

from bumblebee.output import Widget

def assertWidgetAttributes(test, widget):
    test.assertTrue(isinstance(widget, Widget))
    test.assertTrue(hasattr(widget, "full_text"))

class MockOutput(object):
    def start(self):
        pass

    def stop(self):
        pass

    def draw(self, widgets, engine):
        engine.stop()

    def flush(self):
        pass

class MockWidget(object):
    def __init__(self, text):
        self._text = text
        self._module = None

    def set_module(self, name):
        self._module = name

    def update(self, widgets):
        pass

    def module(self):
        return self._module

    def full_text(self):
        return self._text

class MockTheme(object):
    def __init__(self):
        self._prefix = None
        self._suffix = None

    def set_prefix(self, value):
        self._prefix = value

    def set_suffix(self, value):
        self._suffix = value

    def prefix(self, widget):
        return self._prefix

    def suffix(self, widget):
        return self._suffix

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
