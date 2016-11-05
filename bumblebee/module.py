import os
import pkgutil
import importlib

import bumblebee.config
import bumblebee.modules

def modules():
    result = []
    path = os.path.dirname(bumblebee.modules.__file__)
    for mod in [ name for _, name, _ in pkgutil.iter_modules([path])]:
        result.append(ModuleDescription(mod))
    return result

class ModuleDescription(object):
    def __init__(self, name):
        self._name = name
        self._mod =importlib.import_module("bumblebee.modules.{}".format(name))

    def name(self):
        return str(self._name)

    def description(self):
        return getattr(self._mod, "description", self.na)()

    def usage(self):
        return getattr(self._mod, "usage", self.na)()

    def notes(self):
        return getattr(self._mod, "notes", self.na)()

    def na(self):
        return "n/a"

class Module(object):
    def __init__(self, output, config, alias=None):
        self._output = output
        self._alias = alias
        name = "{}.".format(alias if alias else self.__module__.split(".")[-1])
        self._config = bumblebee.config.ModuleConfig(config, name)

    def critical(self, widget):
        return False

    def warning(self, widget):
        return False

    def state(self, widget):
        return "default"

    def instance(self, widget):
        return self._alias if self._alias else self.__module__.split(".")[-1]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
