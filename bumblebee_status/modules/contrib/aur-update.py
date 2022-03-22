"""Check updates for AUR.

Requires the following executable:
    * yay (https://github.com/Jguer/yay)

contributed by `ishaanbhimwal <https://github.com/ishaanbhimwal>`_ - many thanks!
"""

import logging

import core.module
import core.widget
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self.background = True
        self.__packages = 0
        self.__error = False

    @property
    def __format(self):
        return self.parameter("format", "Update AUR: {}")

    def utilization(self, widget):
        return self.__format.format(self.__packages)

    def hidden(self):
        return self.__packages == 0 and not self.__error

    def update(self):
        self.__error = False
        code, result = util.cli.execute(
            "yay -Qum", ignore_errors=True, return_exitcode=True
        )

        if code == 0:
            if result == "":
                self.__packages = 0
            else:
                self.__packages = len(result.strip().split("\n"))
        else:
            self.__error = True
            logging.error("aur-update exited with {}: {}".format(code, result))

    def state(self, widget):
        if self.__error:
            return "warning"
        return self.threshold_state(self.__packages, 1, 100)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
