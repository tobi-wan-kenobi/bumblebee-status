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

    def full_text(self):
        return self._text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
