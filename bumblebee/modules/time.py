from __future__ import absolute_import

import datetime
import bumblebee.module

def usage():
    module = __name__.split(".")[-1]
    if module == "date":
        return "date::<strftime format string, defaults to %x>"
    if module == "time":
        return "time::<strftime format string, defaults to %X>"
    return "datetime::<strftime format string, defaults to '%x %X'>"

def notes():
    return "none"

def description():
    return "Displays the current time, using the optional format string as input for strftime."

class Module(bumblebee.module.Module):
    def __init__(self, output, args):
        super(Module, self).__init__(args)

        module = self.__module__.split(".")[-1]
        default = "%x %X"
        if module == "date":
            default = "%x"
        if module == "time":
            default = "%X"

        self._fmt = args[0] if args else default


    def data(self):
        return datetime.datetime.now().strftime(self._fmt)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
