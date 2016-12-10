"""Core application engine"""

import os
import time
import pkgutil
import importlib
import bumblebee.error
import bumblebee.modules

def all_modules():
    """Return a list of available modules"""
    result = []
    path = os.path.dirname(bumblebee.modules.__file__)
    for mod in [name for _, name, _ in pkgutil.iter_modules([path])]:
        result.append({
            "name": mod
        })
    return result

class Module(object):
    """Module instance base class

    Objects of this type represent the modules that
    the user configures. Concrete module implementations
    (e.g. CPU utilization, disk usage, etc.) derive from
    this base class.
    """
    def __init__(self, engine, config={}, widgets=[]):
        self.name = self.__module__.split(".")[-1]
        self._config = config
        if "name" not in self._config:
            self._config["name"] = self.name
        self.id = self._config["name"]
        self._widgets = []
        if widgets:
            self._widgets = widgets if isinstance(widgets, list) else [widgets]

    def widgets(self):
        """Return the widgets to draw for this module"""
        return self._widgets

    def widget(self, name):
        for widget in self._widgets:
            if widget.name == name:
                return widget

    def update(self, widgets):
        """By default, update() is a NOP"""
        pass

    def parameter(self, name, default=None):
        """Return the config parameter 'name' for this module"""
        name = "{}.{}".format(self._config["name"], name)
        return self._config["config"].get(name, default)

class Engine(object):
    """Engine for driving the application

    This class connects input/output, instantiates all
    required modules and drives the "event loop"
    """
    def __init__(self, config, output=None, inp=None):
        self._output = output
        self._config = config
        self._running = True
        self._modules = []
        self.input = inp
        self.load_modules(config.modules())
        self.input.start()

    def load_modules(self, modules):
        """Load specified modules and return them as list"""
        for module in modules:
            self._modules.append(self._load_module(module["module"], module["name"]))
        return self._modules

    def _load_module(self, module_name, config_name=None):
        """Load specified module and return it as object"""
        if config_name is None:
            config_name = module_name
        try:
            module = importlib.import_module("bumblebee.modules.{}".format(module_name))
        except ImportError as error:
            raise bumblebee.error.ModuleLoadError(error)
        return getattr(module, "Module")(self, {
            "name": config_name,
            "config": self._config
        })

    def running(self):
        """Check whether the event loop is running"""
        return self._running

    def stop(self):
        """Stop the event loop"""
        self._running = False

    def run(self):
        """Start the event loop"""
        self._output.start()
        while self.running():
            self._output.begin()
            for module in self._modules:
                module.update(module.widgets())
                for widget in module.widgets():
                    widget.link_module(module)
                    self._output.draw(widget=widget, module=module, engine=self)
            self._output.flush()
            self._output.end()
            if self.running():
                self.input.wait(self._config.get("interval", 1))

        self._output.stop()
        self.input.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
