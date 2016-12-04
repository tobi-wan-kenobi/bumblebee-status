# pylint: disable=C0103,C0111

class MockWidget(object):
    def __init__(self, text):
        self._text = text

    def text(self):
        return self._text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
