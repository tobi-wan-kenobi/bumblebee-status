import bumblebee.module
import psutil

def usage():
    return "cpu"

def notes():
    return "Warning is at 70%, Critical at 80%."

def description():
    return "Displays CPU utilization across all CPUs."

class Module(bumblebee.module.Module):
    def __init__(self, output, config):
        super(Module, self).__init__(output, config)
        self._perc = psutil.cpu_percent(percpu=False)
        self._config = config

# TODO
#        output.add_callback(module=self.__module__, button=1,
#            cmd="gnome-system-monitor")

    def widgets(self):
        self._perc = psutil.cpu_percent(percpu=False)
        return [
            bumblebee.output.Widget(self,
                "{:05.02f}%".format(self._perc)
            )
        ]

    def warning(self):
        return self._perc > self._config.parameter("cpu.warning", 70)

    def critical(self):
        return self._perc > self._config.parameter("cpu.critical", 80)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
