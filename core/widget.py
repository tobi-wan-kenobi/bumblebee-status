import util.store

class Widget(util.store.Store):
    def __init__(self, full_text):
        self._full_text = full_text

    def full_text(self, value=None):
        if value:
            self._full_text = value
        else:
            if callable(self._full_text):
                return self._full_text()
            return self._full_text

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
