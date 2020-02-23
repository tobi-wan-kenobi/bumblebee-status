import core.input
import util.store

class Widget(util.store.Store, core.input.Object):
    def __init__(self, full_text):
        super(Widget, self).__init__()
        self._full_text = full_text
        self._module = None

    def full_text(self, value=None):
        if value:
            self._full_text = value
        else:
            if callable(self._full_text):
                return self._full_text(self)
        return self._full_text

    def module(self, module):
        self._module = module

    def state(self):
        rv = []
        if self._module:
            rv = self._module.state(self)
        return rv if isinstance(rv, list) else [rv]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
