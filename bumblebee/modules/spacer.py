import bumblebee.module
import bumblebee.util

def usage():
    return "spacer"

def notes():
    return "none"

def description():
    return "Draws an empty field."

class Module(bumblebee.module.Module):
    def __init__(self, output, config):
        super(Module, self).__init__(output, config)

    def widgets(self):
        return bumblebee.output.Widget(self, "")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
