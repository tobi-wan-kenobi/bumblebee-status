# pylint: disable=C0111,R0903

"""Display and run a Pomodoro timer.
Left click to start timer, left click again to pause.
Right click will cancel the timer.
"""

from __future__ import absolute_import
import datetime
from math import ceil

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = bumblebee.output.Widget(full_text=self.text)
        self.work_period = 25
        self.break_period = 5
        self.remaining_time = datetime.timedelta(minutes=self.work_period)
        self.remaining_time_str = "{}m ".format(ceil((self.remaining_time.seconds / 60)))
        # self.remaining_time_str = "{}min{}s ".format(int((self.remaining_time.seconds / 60)),
        #                                              round((self.remaining_time.seconds/60) % 1*60))
        self.time = None
        self.pomodoro = { "state":"OFF", "type": ""}
        self._text = self.remaining_time_str + self.pomodoro["type"]
        super(Module, self).__init__(engine, config, widgets)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd=self.timer_play_pause)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
                                       cmd=self.timer_reset)
        
    def text(self, widget):
        return "{}".format(self._text) 
        
    def update(self, widget):
        if self.pomodoro["state"] == "ON":
            timediff = (datetime.datetime.now() - self.time)
            if timediff.seconds >= 0:
                self.remaining_time -= timediff
                self.time = datetime.datetime.now()

            if self.remaining_time.seconds <= 0:
                if self.pomodoro["type"] == "Work":
                    self.pomodoro["type"] = "Break"
                    self.remaining_time = datetime.timedelta(minutes=self.break_period)
                elif self.pomodoro["type"] == "Break":
                    self.pomodoro["type"] = "Work"
                    self.remaining_time = datetime.timedelta(minutes=self.work_period)

        self.remaining_time_str = "{}m ".format(ceil((self.remaining_time.seconds / 60)))
        # self.remaining_time_str = "{}min{}s ".format(int((self.remaining_time.seconds / 60)),
        #                                             round((self.remaining_time.seconds / 60) % 1 * 60))
        self._text = self.remaining_time_str + self.pomodoro["type"]
    
    def timer_play_pause(self, widget):
        if self.pomodoro["state"] == "OFF":
            self.pomodoro = {"state": "ON", "type": "Work"}
            self.remaining_time = datetime.timedelta(minutes=self.work_period)
            self.time = datetime.datetime.now()
        elif self.pomodoro["state"] == "ON":
            self.pomodoro["state"] = "PAUSED"
            self.remaining_time -= (datetime.datetime.now() - self.time)
            self.time = datetime.datetime.now()
        elif self.pomodoro["state"] == "PAUSED":
            self.pomodoro["state"] = "ON"
            self.time = datetime.datetime.now()

    def timer_reset(self, widget):
        if self.pomodoro["state"] == "ON" or self.pomodoro["state"] == "PAUSED":
            self.pomodoro = {"state":"OFF", "type": "" }
            self.remaining_time = datetime.timedelta(minutes=self.work_period)

    def state(self, widget):
        state = [];
        state.append(self.pomodoro["state"].lower())
        if self.pomodoro["state"] == "ON" or self.pomodoro["state"] == "OFF":
            state.append(self.pomodoro["type"].lower())

        return state
