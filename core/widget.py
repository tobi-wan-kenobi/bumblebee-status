import core.input
import core.decorators
import util.store

class Widget(util.store.Store, core.input.Object):
    def __init__(self, full_text='', name=None, module=None):
        super(Widget, self).__init__()
        self.__full_text = full_text
        self.__module = module
        self.name = name

    def full_text(self, value=None):
        if value:
            self.__full_text = value
        else:
            if callable(self.__full_text):
                return self.__full_text(self)
        return self.__full_text

    def module(self, module=None):
        if not module:
            return self.__module
        self.__module = module

    def state(self):
        rv = []
        if self.get('state', None):
            tmp = self.get('state')
            rv = tmp[:] if isinstance(tmp, list) else [tmp]
        if self.__module:
            tmp = self.__module.state(self)
            rv.extend(tmp if isinstance(tmp, list) else [tmp])
        return rv

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
