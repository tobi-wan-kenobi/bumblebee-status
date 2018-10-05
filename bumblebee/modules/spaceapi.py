# pylint: disable=C0111,R0903

"""Displays the state of a spaceapi endpoint

Requires the following libraries:
    * urllib
    * json
    * time

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.name: String overwriting the space name
    * spaceapi.prefix: Prefix for the space string
    * spaceapi.interval: time between updates
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import urllib.request
import json
import time


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine, config, bumblebee.output.Widget(full_text=self.getState)
        )
        self._state = False
        self._error = False
        self._url = self.parameter("url",
                                   default="http://club.entropia.de/spaceapi")
        self._name = self.parameter("name", default="")
        self._lastQuery = 0
        self._sleeptime = self.parameter("interval", default=300)

    def getState(self, widget):
        string = self.parameter("prefix", default="")
        string += self._name + ": "
        if self._error:
            string += "ERROR"
        elif self._state:
            string += "Open"
        else:
            string += "Closed"
        return string

    def state(self, widget):
        if self._error:
            return ["critical"]
        elif self._state:
            return ["warning"]
        else:
            return []

    def update(self, widgets):
        unixtime = time.mktime(time.gmtime())
        # Only query again after interval has passed
        if self._lastQuery + self._sleeptime < int(unixtime):
            self._lastQuery = int(unixtime)
            try:
                with urllib.request.urlopen(self._url) as u:
                    data = json.loads(u.read().decode())
                    self._state = data["state"]["open"]
                    self._name = self.parameter("name", default=data["space"])
                    self._error = False
            except Exception:
                # Displays ERROR status
                self._error = True


# Author: Tobias Manske <tobias.manske@mailbox.org>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
