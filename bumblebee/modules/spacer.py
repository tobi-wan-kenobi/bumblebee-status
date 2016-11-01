import bumblebee.module
import bumblebee.util

def usage():
    return "spacer"

def notes():
    return "none"

def description():
    return "Draws an empty field."

class Module(bumblebee.module.Module):
    def __init__(self, output, args):
        super(Module, self).__init__(args)

    def data(self):
        return ""

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
