import bumblebee.module
import multiprocessing
import os

def description():
    return "Displays system load."

def parameters():
    return [
        "load.warning: Warning threshold for the one-minute load average (defaults to 70% of the number of CPUs)",
        "load.critical: Critical threshold for the one-minute load average (defaults 80% of the number of CPUs)"
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._cpus = 1
        try:
            self._cpus = multiprocessing.cpu_count()
        except multiprocessing.NotImplementedError as e:
            pass

        output.add_callback(module=self.instance(), button=1, cmd="gnome-system-monitor")

    def widgets(self):
        self._load = os.getloadavg()

        return bumblebee.output.Widget(self, "{:.02f}/{:.02f}/{:.02f}".format(
            self._load[0], self._load[1], self._load[2]))

    def warning(self, widget):
        return self._load[0] > self._config.parameter("warning", self._cpus*0.7)

    def critical(self, widget):
        return self._load[0] > self._config.parameter("critical", self._cpus*0.8)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
