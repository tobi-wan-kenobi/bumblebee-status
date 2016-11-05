import bumblebee.module
import psutil

def description():
    return "Displays CPU utilization across all CPUs."

def parameters():
    return [
        "cpu.warning: Warning threshold in % of disk usage (defaults to 70%)",
        "cpu.critical: Critical threshold in % of disk usage (defaults to 80%)",
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._perc = psutil.cpu_percent(percpu=False)

        output.add_callback(module=self.instance(), button=1, cmd="gnome-system-monitor")

    def widgets(self):
        self._perc = psutil.cpu_percent(percpu=False)
        return bumblebee.output.Widget(self, "{:05.02f}%".format(self._perc))

    def warning(self, widget):
        return self._perc > self._config.parameter("warning", 70)

    def critical(self, widget):
        return self._perc > self._config.parameter("critical", 80)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
