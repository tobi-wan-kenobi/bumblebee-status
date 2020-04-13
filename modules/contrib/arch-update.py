"""Check updates to Arch Linux.

Requires the following executable:
    * checkupdates (from pacman-contrib)

"""
import core.module
import core.widget
import core.decorators

import util.cli

class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config):
        super().__init__(config, core.widget.Widget(self.utilization))
        self.__packages = None

    @property
    def __format(self):
        return self.parameter('format', 'Update Arch: {}')

    def utilization(self, widget):
        return self.__format.format(self.__packages)

    def hidden(self):
        return self.check_updates() == 0

    def update(self):
        result = util.cli.execute('checkupdates')
        self.__packages = len(result.split('\n')) - 1

    def state(self, widget):
        return self.threshold_state(self.__packages, 1, 100)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
