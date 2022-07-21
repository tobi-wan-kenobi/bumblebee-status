# pylint: disable=C0111,R0903

"""Display and run a Pomodoro timer.
Left click to start timer, left click again to pause.
Right click will cancel the timer.

Parameters:
    * pomodoro.work: The work duration of timer in minutes (defaults to 25)
    * pomodoro.break: The break duration of timer in minutes (defaults to 5)
    * pomodoro.format: Timer display format with '%m' and '%s' for minutes and seconds (defaults to '%m:%s')
      Examples: '%m min %s sec', '%mm', '', 'timer'
    * pomodoro.notify: Notification command to run when timer ends/starts (defaults to nothing)
      Example: 'notify-send 'Time up!''. If you want to chain multiple commands,
      please use an external wrapper script and invoke that. The module itself does
      not support command chaining (see https://github.com/tobi-wan-kenobi/bumblebee-status/issues/532
      for a detailed explanation)

contributed by `martindoublem <https://github.com/martindoublem>`_, inspired by `karthink <https://github.com/karthink>`_ - many thanks!
"""

from __future__ import absolute_import
import datetime
from math import ceil

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.text))

        # Parameters
        self.__work_period = int(self.parameter("work", 25))
        self.__break_period = int(self.parameter("break", 5))
        self.__time_format = self.parameter("format", "%m:%s")
        self.__notify_cmd = self.parameter("notify", "")

        # TODO: Handle time formats more gracefully. This is kludge.
        self.display_seconds_p = False
        self.display_minutes_p = False
        if "%s" in self.__time_format:
            self.display_seconds_p = True
        if "%m" in self.__time_format:
            self.display_minutes_p = True

        self.remaining_time = datetime.timedelta(minutes=self.__work_period)

        self.time = None
        self.pomodoro = {"state": "OFF", "type": ""}
        self.__text = self.remaining_time_str() + self.pomodoro["type"]

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.timer_play_pause
        )
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.timer_reset)

    def remaining_time_str(self):
        if self.display_seconds_p and self.display_minutes_p:
            minutes, seconds = divmod(self.remaining_time.seconds, 60)
        if not self.display_seconds_p:
            minutes = ceil(self.remaining_time.seconds / 60)
            seconds = 0
        if not self.display_minutes_p:
            minutes = 0
            seconds = self.remaining_time.seconds

        minutes = "{:2d}".format(minutes)
        seconds = "{:02d}".format(seconds)
        return self.__time_format.replace("%m", minutes).replace("%s", seconds) + " "

    def text(self, widget):
        return "{}".format(self.__text)

    def update(self):
        if self.pomodoro["state"] == "ON":
            timediff = datetime.datetime.now() - self.time
            if timediff.seconds >= 0:
                self.remaining_time -= timediff
                self.time = datetime.datetime.now()

            if self.remaining_time.total_seconds() <= 0:
                self.notify()
                if self.pomodoro["type"] == "Work":
                    self.pomodoro["type"] = "Break"
                    self.remaining_time = datetime.timedelta(
                        minutes=self.__break_period
                    )
                elif self.pomodoro["type"] == "Break":
                    self.pomodoro["type"] = "Work"
                    self.remaining_time = datetime.timedelta(minutes=self.__work_period)

        self.__text = self.remaining_time_str() + self.pomodoro["type"]

    def notify(self):
        if self.__notify_cmd:
            util.cli.execute(self.__notify_cmd)

    def timer_play_pause(self, widget):
        if self.pomodoro["state"] == "OFF":
            self.pomodoro = {"state": "ON", "type": "Work"}
            self.remaining_time = datetime.timedelta(minutes=self.__work_period)
            self.time = datetime.datetime.now()
        elif self.pomodoro["state"] == "ON":
            self.pomodoro["state"] = "PAUSED"
            self.remaining_time -= datetime.datetime.now() - self.time
            self.time = datetime.datetime.now()
        elif self.pomodoro["state"] == "PAUSED":
            self.pomodoro["state"] = "ON"
            self.time = datetime.datetime.now()

    def timer_reset(self, widget):
        if self.pomodoro["state"] == "ON" or self.pomodoro["state"] == "PAUSED":
            self.pomodoro = {"state": "OFF", "type": ""}
            self.remaining_time = datetime.timedelta(minutes=self.__work_period)

    def state(self, widget):
        state = []
        state.append(self.pomodoro["state"].lower())
        if self.pomodoro["state"] == "ON" or self.pomodoro["state"] == "OFF":
            state.append(self.pomodoro["type"].lower())

        return state


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
