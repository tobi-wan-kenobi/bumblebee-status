import datetime
import bumblebee.module

class Module(bumblebee.module.Module):
    def __init__(self, theme, args):
        super(Module, self).__init__(theme, args)

    def data(self):
        return datetime.datetime.now().strftime("%x %X")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
