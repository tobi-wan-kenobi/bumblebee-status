import importlib
import logging

import core.input
import core.widget
import core.decorators

try:
    error = ModuleNotFoundError('')
except Exception as e:
    ModuleNotFoundError = Exception

log = logging.getLogger(__name__)

def load(module_name, config=None):
    error = None
    for namespace in [ 'core', 'contrib' ]:
        try:
            mod = importlib.import_module('modules.{}.{}'.format(namespace, module_name))
            return getattr(mod, 'Module')(config)
        except ModuleNotFoundError as e:
            log.fatal('failed to import {}: {}'.format(module_name, e))
        except ImportError as e:
            log.fatal('failed to import {}: {}'.format(module_name, e))
            error = str(e)
    if not error:
        error = 'No such module'
    log.fatal('failed to import {}: {}'.format(module_name, error))
    return Error(config, module_name, error)

class Module(core.input.Object):
    def __init__(self, config=None, widgets=[]):
        super().__init__()
        self._config = config
        self._widgets = widgets if isinstance(widgets, list) else [ widgets ]
        for widget in self._widgets:
            widget.module(self)
        self._name = None
        self.next_update = None

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

    def update_wrapper(self):
        try:
            self.update()
        except Exception as e:
            module = Error(self._config, 'error', str(e))
            self._widgets = [module.widget()]
            self.update = module.update

    def name(self):
        return self._name if self._name else self.module_name()

    def module_name(self):
        return self.__module__.split('.')[-1]

    def widgets(self, widgets=None):
        if widgets:
            self._widgets = widgets
        return self._widgets

    def widget(self, name=None):
        if not name: return self.widgets()[0]

        for w in self.widgets():
            if w.name() == name: return w
        return None

    def state(self, widget):
        return []

    def threshold_state(self, value, warn, crit):
        if value > float(self.parameter('critical', crit)):
            return 'critical'
        if value > float(self.parameter('warning', warn)):
            return 'warning'
        return None

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

    def state(self, widget):
        return ['critical']

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
