# pylint: disable=C0111,R0903

"""Shows bumblebee-status errors"""

import platform

import core.module
import core.widget
import core.event


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__error = ""
        self.__state = "critical"

        core.event.register("error", self.__set_error)

    def full_text(self, widgets):
        return self.__error

    def __set_error(self, error="n/a", state="critical"):
        self.__error = error
        self.__state = state

    def state(self, widget):
        if self.__error:
            return [self.__state]
        return []


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
