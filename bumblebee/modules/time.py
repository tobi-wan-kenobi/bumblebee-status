from __future__ import absolute_import

import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, args):
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
