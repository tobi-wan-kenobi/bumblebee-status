# pylint: disable=C0111,R0903

"""Displays two widgets that can be used to scroll the whole status bar

Parameters:
    * scroll.width: Width (in number of widgets) to display
"""

import core.module
import core.widget
import core.input
import core.event

import util.format

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, [])
        self.__offset = 0
        self.__widgetcount = 0
        w = self.add_widget(full_text = "<")
        core.input.register(w, button=core.input.LEFT_MOUSE, cmd=self.scroll_left)
        w = self.add_widget(full_text = ">")
        core.input.register(w, button=core.input.LEFT_MOUSE, cmd=self.scroll_right)
        self.__width = util.format.asint(self.parameter("width"))
        config.set("output.width", self.__width)
        core.event.register("output.done", self.update_done)


    def scroll_left(self, _):
        if self.__offset > 0:
            core.event.trigger("output.scroll-left")

    def scroll_right(self, _):
        if self.__offset + self.__width < self.__widgetcount:
            core.event.trigger("output.scroll-right")

    def update_done(self, offset, widgetcount):
        self.__offset = offset
        self.__widgetcount = widgetcount

    def scroll(self):
        return False

    def state(self, widget):
        if widget.id == self.widgets()[0].id:
            if self.__offset == 0:
                return ["warning"]
        elif self.__offset + self.__width >= self.__widgetcount:
            return ["warning"]
        return []

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
