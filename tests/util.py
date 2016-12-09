# pylint: disable=C0103,C0111,W0613

from bumblebee.output import Widget

def assertWidgetAttributes(test, widget):
    test.assertTrue(isinstance(widget, Widget))
    test.assertTrue(hasattr(widget, "full_text"))

class MockEngine(object):
    pass

class MockOutput(object):
    def start(self):
        pass

    def stop(self):
        pass

    def draw(self, widget, engine):
        engine.stop()

    def begin(self):
        pass

    def flush(self):
        pass

    def end(self):
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
        self._fg = None
        self._bg = None

    def set_prefix(self, value):
        self._prefix = value

    def set_suffix(self, value):
        self._suffix = value

    def set_fg(self, value):
        self._fg = value

    def set_bg(self, value):
        self._bg = value

    def prefix(self, widget):
        return self._prefix

    def suffix(self, widget):
        return self._suffix

    def fg(self, widget):
        return self._fg

    def bg(self, widget):
        return self._bg

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
