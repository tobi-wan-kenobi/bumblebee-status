# pylint: disable=C0111,R0903,W1401

r""" Execute command in shell and print result

Few command examples:
    'ping -c 1 1.1.1.1 | grep -Po '(?<=time=)\d+(\.\d+)? ms''
    'echo 'BTC=$(curl -s rate.sx/1BTC | grep -Po \'^\d+\')USD''
    'curl -s https://wttr.in/London?format=%l+%t+%h+%w'
    'pip3 freeze | wc -l'
    'any_custom_script.sh | grep arguments'

Parameters:
    * shell.command:  Command to execute
      Use single parentheses if evaluating anything inside (sh-style)
      For example shell.command='echo $(date +'%H:%M:%S')'
      But NOT shell.command='echo $(date +'%H:%M:%S')'
      Second one will be evaluated only once at startup
    * shell.left_click_command:  Command to execute on
      left mouse button click. Clicked commands are always
      executed synchronously.
      Command formatting rules described above applies here
    * shell.right_click_command:  Command to execute on
      right mouse button click. See above.
    * shell.interval: Update interval in seconds
      (defaults to 1s == every bumblebee-status update)
    * shell.async:    Run update in async mode. Won't run next thread if
      previous one didn't finished yet. Useful for long
      running scripts to avoid bumblebee-status freezes
      (defaults to False)

contributed by `rrhuffy <https://github.com/rrhuffy>`_ - many thanks!
"""

import os
import subprocess
import threading
import functools
import logging
import sys

import core.module
import core.widget
import core.input
import core.event
import util.format
import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        self.widget = core.widget.Widget(self.get_output)
        super().__init__(config, theme, self.widget)

        self.__command = self.parameter("command", 'echo "no command configured"')
        self.__left_click_command = self.parameter(
            "left_click_command",
            'echo "no left_click_command configured"')
        self.__right_click_command = self.parameter(
            "right_click_command",
            'echo "no right_click_command configured"')
        self.__async = util.format.asbool(self.parameter("async"))

        if self.__async:
            self.__output = "please wait..."
            self.__current_thread = threading.Thread()

        if self.parameter("scrolling.makewide") is None:
            self.set("scrolling.makewide", False)

        if self.__left_click_command is not None:
            core.input.register(
                self.widget,
                button=core.input.LEFT_MOUSE,
                cmd=functools.partial(
                    self.click_command,
                    command=self.__left_click_command))
        if self.__right_click_command is not None:
            core.input.register(
                self.widget,
                button=core.input.RIGHT_MOUSE,
                cmd=functools.partial(
                    self.click_command,
                    command=self.__right_click_command))

    def set_output(self, value):
        self.__output = value

    def click_command(self, event, command=None):
        util.cli.execute(command, shell=True, ignore_errors=True, wait=True)
        core.event.trigger("update", [self.id], redraw_only=True)

    @core.decorators.scrollable
    def get_output(self, _):
        return self.__output

    def update(self):
        # if requested then run not async version and just execute command in this thread
        if not self.__async:
            self.set_output(
                util.cli.execute(self.__command, shell=True, ignore_errors=True).strip()
            )
            return

        # if previous thread didn't end yet then don't do anything
        if self.__current_thread.is_alive():
            return

        # spawn new thread to execute command and pass callback method to get output from it
        self.__current_thread = threading.Thread(
            target=lambda obj, cmd: obj.set_output(
                util.cli.execute(cmd, ignore_errors=True)
            ),
            args=(self, self.__command),
        )
        self.__current_thread.start()

    def state(self, _):
        if self.__output == "no command configured":
            return "warning"


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
