import psutil
import bumblebee.module
import bumblebee.util

def description():
    return "Shows available RAM, total amount of RAM and the percentage of available RAM."

def parameters():
    return [
        "memory.warning: Warning threshold in % of memory still available (defaults to 20%)",
        "memory.critical: Critical threshold in % of memory still available (defaults to 10%)",
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._mem = psutil.virtual_memory()

        output.add_callback(module=self.instance(), button=1, cmd="gnome-system-monitor")

    def widgets(self):
        self._mem = psutil.virtual_memory()

        used = self._mem.total - self._mem.available

        return bumblebee.output.Widget(self, "{}/{} ({:05.02f}%)".format(
            bumblebee.util.bytefmt(used),
            bumblebee.util.bytefmt(self._mem.total),
            self._mem.percent)
        )

    def warning(self, widget):
        return self._mem.percent < self._config.parameter("warning", 20)

    def critical(self, widget):
        return self._mem.percent < self._config.parameter("critical", 10)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
