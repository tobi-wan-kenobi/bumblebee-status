"""Check updates to Arch Linux.

Requires the following executable:
    * checkupdates (from pacman-contrib)

"""


import subprocess
import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.utilization)
        super(Module, self).__init__(engine, config, widget)
        self.packages = self.check_updates()

    def check_updates(self):
        p = subprocess.Popen(
                "checkupdates", stdout=subprocess.PIPE, shell=True)

        p_status = p.wait()

        if p_status == 0:
            (output, err) = p.communicate()

            output = output.decode('utf-8')
            packages = output.split('\n')
            packages.pop()

            return len(packages)
        return 0

    @property
    def _format(self):
        return self.parameter("format", "Update Arch: {}")

    def utilization(self, widget):
        return self._format.format(self.packages)

    def hidden(self):
        return self.check_updates() == 0

    def update(self, widgets):
        self.packages = self.check_updates()

    def state(self, widget):
        return self.threshold_state(self.packages, 1, 100)
