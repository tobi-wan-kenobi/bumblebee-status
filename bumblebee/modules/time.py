import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, args):
        self._fmt = args[0] if args else "%x %X"
        super(Module, self).__init__(args)

    def data(self):
        return datetime.datetime.now().strftime(self._fmt)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
