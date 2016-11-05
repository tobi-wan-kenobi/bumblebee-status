from __future__ import absolute_import

import datetime
import bumblebee.module

def description():
    return "Displays the current time, using the optional format string as input for strftime."

def parameters():
    module = __name__.split(".")[-1]
    return [
        "{}.format: strftime specification (defaults to {})".format(module, default_format(module))
    ]

def default_format(module):
    default = "%x %X"
    if module == "date":
        default = "%x"
    if module == "time":
        default = "%X"
    return default

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)

        module = self.__module__.split(".")[-1]

        self._fmt = self._config.parameter("format", default_format(module))

    def widgets(self):
        return bumblebee.output.Widget(self, datetime.datetime.now().strftime(self._fmt))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
