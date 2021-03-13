import logging

import core.input
import core.decorators

import util.store
import util.format

log = logging.getLogger(__name__)


class Widget(util.store.Store, core.input.Object):
    def __init__(self, full_text="", name=None, widget_id=None, hidden=False):
        super(Widget, self).__init__()
        self.__full_text = full_text
        self.module = None
        self.name = name
        self.id = widget_id or self.id
        self.hidden = hidden

    @property
    def module(self):
        return self.__module

    @module.setter
    def module(self, module):
        self.__module = module

        if self.index() < 0:
            return

        if module:
            custom_ids = util.format.aslist(module.parameter("id"))
            if len(custom_ids) > self.index():
                self.id = custom_ids[self.index()]
            if util.format.asbool(module.parameter("scrolling", False)) == True:
                if callable(self.__full_text):
                    self.__full_text = core.decorators.scrollable(
                        self.__full_text.__func__
                    ).__get__(module)
                else:
                    log.warning("unable to make scrollable: {}".format(module.name))

    def index(self):
        if not self.module:
            return 0

        idx = 0
        for w in self.module.widgets():
            if w.id == self.id:
                return idx
            idx = idx + 1
        return -1  # not found

    def theme(self, attribute):
        attr = "theme.{}".format(attribute)
        if self.module:
            param = util.format.aslist(self.module.parameter(attr))
            if param and len(param) > self.index():
                return param[self.index()]
        return self.get(attr)

    def full_text(self, value=None):
        if value:
            self.__full_text = value
        else:
            if callable(self.__full_text):
                return self.__full_text(self)
        return self.__full_text

    def state(self):
        rv = []
        if self.get("state", None):
            tmp = self.get("state")
            rv = tmp[:] if isinstance(tmp, list) else [tmp]
        if self.module:
            tmp = self.module.state(self)
            rv.extend(tmp if isinstance(tmp, list) else [tmp])
        return rv


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
