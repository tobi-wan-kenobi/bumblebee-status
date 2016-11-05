import os
import pkgutil
import importlib

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
    def __init__(self, args):
        pass

    def data(self):
        pass

    def critical(self):
        return False

    def warning(self):
        return False

    def state(self):
        return "default"

    def next(self):
        return False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
