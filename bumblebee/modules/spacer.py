import bumblebee.module
import bumblebee.util

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)

    def data(self):
        return ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
