# pylint: disable=C0111,R0903

"""Performs a speedtest - only updates when the "play" button is clicked

Requires the following python module:
    * speedtest-cli

"""

import sys

import core.module
import core.widget
import core.input
import core.event
import core.decorators

import speedtest


class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.background = True
        self.__result = "<speedtest>"
        self.__running = False

        start = self.add_widget(name="start")
        main = self.add_widget(name="main", full_text=self.result)

        core.input.register(start, button=core.input.LEFT_MOUSE, cmd=self.update_event)

    def result(self, _):
        return self.__result

    def update_event(self, _):
        self.__running = True
        self.update()

    def update(self):
        if not self.__running:
            return
        core.event.trigger("update", [self.id], redraw_only=True)
        s = speedtest.Speedtest()
        s.get_best_server()
        s.download(threads=None)
        s.upload(threads=None)

        self.__result = "ping: {:.2f}ms down: {:.2f}Mbps up: {:.2f}Mbps".format(
            s.results.ping,
            s.results.download / 1024 / 1024,
            s.results.upload / 1024 / 1024,
        )
        self.__running = False
        core.event.trigger("update", [self.id], redraw_only=True)

    def state(self, widget):
        if widget.name == "start":
            return "running" if self.__running else "not-running"
        return None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
