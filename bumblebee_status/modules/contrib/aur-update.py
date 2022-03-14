"""Check updates for AUR.

Requires the following packages:
    * yay (used as default)

Note - You can replace yay by changing the "yay -Qum"
command for your preferred AUR helper. Few examples:

paru -Qum
pikaur -Qua
rua upgrade --printonly
trizen -Su --aur --quiet
yay -Qum

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
            self.__packages = len(result.strip().split("\n"))
        elif code == 2:
            self.__packages = 0
        else:
            self.__error = True
            logging.error("yay -Qum exited with {}: {}".format(code, result))

    def state(self, widget):
        if self.__error:
            return "warning"
        return self.threshold_state(self.__packages, 1, 100)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
