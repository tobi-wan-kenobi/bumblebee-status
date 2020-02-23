import importlib
import logging

import core.input
import core.widget
import core.decorators

log = logging.getLogger(__name__)

def load(module_name, config=None):
    try:
        mod = importlib.import_module('modules.{}'.format(module_name))
    except ImportError as error:
        log.fatal('failed to import {}: {}'.format(module_name, error))
        return Error(config, module_name, error)
    return getattr(mod, 'Module')(config)

class Module(core.input.Object):
    def __init__(self, config=None, widgets=[]):
        super().__init__()
        self._config = config
        self._widgets = widgets if isinstance(widgets, list) else [ widgets ]
        self._name = None

    def parameter(self, key, default=None):
        value = default

        for prefix in [ self.name(), self.module_name() ]:
            value = self._config.get('{}.{}'.format(prefix, key), value)
        # TODO retrieve from config file
        return value

    def set(self, key, value):
        self._config.set('{}.{}'.format(self.name(), key), value)

    def update(self):
        pass

    def name(self):
        return self._name if self._name else self.module_name()

    def module_name(self):
        return self.__module__.split('.')[-1]

    def widgets(self):
        return self._widgets

class Error(Module):
    def __init__(self, config, module, error):
        super().__init__(config, core.widget.Widget(self.full_text))
        self._module = module
        self._error = error

        self.set('scrolling.bounce', False)
        self.set('scrolling.speed', 2)
        self.set('width', 15)

    @core.decorators.scrollable
    def full_text(self, widget):
        return '{}: {}'.format(self._module, self._error)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
