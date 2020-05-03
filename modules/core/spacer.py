# pylint: disable=C0111,R0903

"""Draws a widget with configurable text content.

Parameters:
    * spacer.text: Widget contents (defaults to empty string)
"""

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))
        self.__text = self.parameter("text", "")

    def text(self, _):
        return self.__text


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
