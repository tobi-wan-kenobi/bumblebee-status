"""Shows User and Hostname in linux

contributed by `Jakepys <https://github.com/JuanPerdomo00>` 

- with much love :)
"""

import core.module
import core.widget
import getpass
import platform


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__username = getpass.getuser()
        self.__hostname = platform.node()

    def full_text(self, widgets):
        return "{}/{}".format(self.__hostname, self.__username)
