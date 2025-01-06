# pylint: disable=C0111,R0903

"""Creates an empty widget that changes width on a timer,
to reduce changes o OLED burn-in from other bumblebee modules.

You should put this module as the last one,
so all the other modules are moved when this one changes in width

contributed by `TheEdgeOfRage <https://github.com/TheEdgeOfRage>`_ - many thanks!
"""

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.content))
        self.__offset = 0

    def content(self, _):
        return self.__offset * " "

    def update(self):
        self.__offset = (self.__offset + 1) % 3
