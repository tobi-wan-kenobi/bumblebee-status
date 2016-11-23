import subprocess
import shlex

import bumblebee.module

def description():
    return "Enable/disable auto screen lock."

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)
        self._activated = 0
        # output.add_callback(module="caffeine.activate", button=1, cmd='notify-send "Consuming caffeine"; xset s off')
        # output.add_callback(module="caffeine.deactivate", button=1, cmd='notify-send "Out of coffee"; xset s 600 600')
        output.add_callback(module="caffeine.activate", button=1, cmd='xset s off')
        output.add_callback(module="caffeine.deactivate", button=1, cmd='xset s default')

    def widgets(self):
        output = subprocess.check_output(shlex.split("xset q"))
        xset_out = output.decode().split("\n")
        for line in xset_out:
            if line.startswith("  timeout"):
                timeout = int(line.split(" ")[4])
                if timeout == 0:
                    self._activated = 1;
                else:
                    self._activated = 0;
                break

        if self._activated == 0:
            return bumblebee.output.Widget(self, "", instance="caffeine.activate")
        elif self._activated == 1:
            return bumblebee.output.Widget(self, "", instance="caffeine.deactivate")

    def state(self, widget):
        if self._activated == 1:
            return "activated"
        else:
            return "deactivated"

