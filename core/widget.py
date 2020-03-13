import core.input
import core.decorators
import util.store

class Widget(util.store.Store, core.input.Object):
    def __init__(self, full_text='', name=None, module=None):
        super(Widget, self).__init__()
        self._full_text = full_text
        self._module = module
        self._name = name

    def name(self):
        return self._name

    def full_text(self, value=None):
        if value:
            self._full_text = value
        else:
            if callable(self._full_text):
                return self._full_text(self)
        return self._full_text

    def module(self, module=None):
        if not module:
            return self._module
        self._module = module

    def state(self):
        rv = []
        if self.get('state', None):
            tmp = self.get('state')
            if isinstance(tmp, list):
                rv.extend(tmp)
            else:
                rv.append(tmp)
        if self._module:
            tmp = self._module.state(self)
            if isinstance(tmp, list):
                rv.extend(tmp)
            else:
                rv.append(tmp)
        return rv if isinstance(rv, list) else [rv]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
