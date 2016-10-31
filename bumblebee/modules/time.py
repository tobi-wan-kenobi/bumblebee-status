import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, args):
        module = self.__module__.split(".")[-1]

        default = "%x" if module == "date" else "%X"
        self._fmt = args[0] if args else default

        super(Module, self).__init__(args)

    def data(self):
        return datetime.datetime.now().strftime(self._fmt)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
