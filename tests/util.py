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
        self.module = None

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

    def reset(self):
        pass

    def prefix(self, widget):
        return self.attr_prefix

    def suffix(self, widget):
        return self.attr_suffix

    def fg(self, widget):
        return self.attr_fg

    def bg(self, widget):
        return self.attr_bg

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
