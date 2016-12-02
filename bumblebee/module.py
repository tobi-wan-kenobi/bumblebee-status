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
        return getattr(self._mod, "description", lambda: "n/a")()

    def parameters(self):
        return getattr(self._mod, "parameters", lambda: [ "n/a" ])()

class Module(object):
    def __init__(self, output, config):
        self._output = output
        self._config = config

    def register_callbacks(self):
        buttons = [
            { "name": "left-click", "id": 1 },
            { "name": "middle-click", "id": 2 },
            { "name": "right-click", "id": 3 },
            { "name": "wheel-up", "id": 4 },
            { "name": "wheel-down", "id": 5 },
        ]
        for button in buttons:
            if self._config.parameter(button["name"], None):
                output.add_callback(
                    module=self.instance(),
                    button=button["id"],
                    cmd=self._config.parameter(button["name"])
                )

    def critical(self, widget):
        return False

    def warning(self, widget):
        return False

    def state(self, widget):
        return "default"

    def instance(self, widget=None):
        return self._config.prefix()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
