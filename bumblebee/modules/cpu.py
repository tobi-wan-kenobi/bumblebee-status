import bumblebee.module
import psutil

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)
        self._perc = psutil.cpu_percent(percpu=False)

    def data(self):
        self._perc = psutil.cpu_percent(percpu=False)

        return "{:05.02f}%".format(self._perc)

    def warning(self):
        return self._perc > 70

    def critical(self):
        return self._perc > 80

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
