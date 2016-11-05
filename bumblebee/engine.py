import importlib
import bumblebee.theme
import bumblebee.output
import bumblebee.modules

class Engine:
    def __init__(self, config):
        self._modules = []
        self._config = config
        self._theme = bumblebee.theme.Theme(config)
        self._output = bumblebee.output.output(config)

    def load_module(self, modulespec):
        name = modulespec["name"]
        module = importlib.import_module("bumblebee.modules.{}".format(name))
        return getattr(module, "Module")(self._output, self._config, modulespec["alias"])

    def load_modules(self):
        for m in self._config.modules():
            self._modules.append(self.load_module(m))

    def run(self):
        self._output.start()

        while True:
            self._theme.begin()
            for m in self._modules:
                self._output.draw(m.widgets(), self._theme)
            self._output.flush()
            self._output.wait()

        self._output.stop()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
