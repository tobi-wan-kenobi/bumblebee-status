import psutil
import bumblebee.module
import bumblebee.util

def usage():
    return "memory"

def notes():
    return "Warning is at 20% available RAM, Critical at 10%."

def description():
    return "Shows available RAM, total amount of RAM and the percentage of available RAM."

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)
        self._mem = psutil.virtual_memory()

    def data(self):
        self._mem = psutil.virtual_memory()

        free = self._mem.available
        total = self._mem.total

        return "{}/{} ({:05.02f}%)".format(bumblebee.util.bytefmt(self._mem.available), bumblebee.util.bytefmt(self._mem.total), 100.0 - self._mem.percent)

    def warning(self):
        return self._mem.percent < 20

    def critical(self):
        return self._mem.percent < 10

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
