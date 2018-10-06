# pylint: disable=C0111,R0903

"""Displays the state of a spaceapi endpoint

Requires the following libraries:
    * requests

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.name: String overwriting the space name
    * spaceapi.prefix: Prefix for the space string
    * spaceapi.interval: time between updates in minutes
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import requests


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine, config, bumblebee.output.Widget(full_text=self.getState)
        )

        # Represents the state of the hackerspace
        self._open = False
        # Set to true if there was an error calling the spaceapi
        self._error = False
        # The URL representing the api endpoint
        self._url = self.parameter("url",
                                   default="http://club.entropia.de/spaceapi")
        # Space Name, can be set manually in case of multiple widgets,
        # so you're able to distinguish
        self._name = self.parameter("name", default="")

        # Only execute every 5 minutes by default
        self.interval(self.parameter("interval", default=5))

    def getState(self, widget):
        text = self.parameter("prefix", default="")
        text += self._name + ": "

        if self._error:
            text += "ERROR"
        elif self._open:
            text += "Open"
        else:
            text += "Closed"
        return text

    def state(self, widget):
        if self._error:
            return ["critical"]
        elif self._open:
            return ["warning"]
        else:
            return []

    def update(self, widgets):
        try:
            with requests.get(self._url) as u:
                json = u.json()
                self._open = json["state"]["open"]
                self._name = self.parameter("name", default=json["space"])
                self._error = False
        except Exception:
            # Displays ERROR status
            self._error = True


# Author: Tobias Manske <tobias.manske@mailbox.org>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
