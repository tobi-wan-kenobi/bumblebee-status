"""Core application engine"""

import time
import importlib
import bumblebee.error

class Module(object):
    """Module instance base class

    Objects of this type represent the modules that
    the user configures. Concrete module implementations
    (e.g. CPU utilization, disk usage, etc.) derive from
    this base class.
    """
    def __init__(self, engine):
        pass

class Engine(object):
    """Engine for driving the application

    This class connects input/output, instantiates all
    required modules and drives the "event loop"
    """
    def __init__(self, config, output=None):
        self._output = output
        self._running = True
        self._modules = []
        self.load_modules(config.modules())

    def load_modules(self, modules):
        """Load specified modules and return them as list"""
        for module in modules:
            self._modules.append(self.load_module(module["module"]))
        return self._modules

    def load_module(self, module_name):
        """Load specified module and return it as object"""
        try:
            module = importlib.import_module("bumblebee.modules.{}".format(module_name))
        except ImportError as error:
            raise bumblebee.error.ModuleLoadError(error)
        return getattr(module, "Module")(self)

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
            widgets = []
            for module in self._modules:
                widgets += module.widgets()
            self._output.draw(widgets)
            self._output.flush()
            time.sleep(1)

        self._output.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
