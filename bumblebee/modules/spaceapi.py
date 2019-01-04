# pylint: disable=C0111,R0903

"""Displays the state of a spaceapi endpoint

Requires the following libraries:
    * requests

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.format: Format string for the output
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import requests
import threading
import sys


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine, config, bumblebee.output.Widget(full_text=self.getState)
        )

        self._data = {}
        self._error = None

        self._threadingCount = 0

        # The URL representing the api endpoint
        self._url = self.parameter("url", default="http://club.entropia.de/spaceapi")
        self._format = self.parameter("format", default=" %%space%%: %%state%%")

    def state(self, widget):
        try:
            if self._error is not None:
                return ["critical"]
            elif self._data['state']['open']:
                return ["warning"]
            else:
                return []
        except KeyError:
            return ["critical"]

    def update(self, widgets):
        if self._threadingCount == 0:
            thread = threading.Thread(target=self.get_api_async, args=())
            thread.start()
        self._threadingCount = (
            0 if self._threadingCount > 300 else self._threadingCount + 1
        )

    def getState(self, widget):
        text = self._format
        if self._error is not None:
            text = self._error
        else:
            try:
                text = text.replace("%%space%%", self._data['space'])
                if self._data['state']['open']:
                    text = text.replace("%%state%%", "Open")
                else:
                    text = text.replace("%%state%%", "Closed")
            except KeyError:
                text = "KeyError"
        return text

    def get_api_async(self):
        try:
            with requests.get(self._url, timeout=10) as u:
                self._data = u.json()
                self._error = None
        except requests.exceptions.Timeout:
            self._error = "Timeout"
        except requests.exceptions.HTTPError:
            self._error = "HTTP Error"
        #  except Exception:
        #      self._error = "CRITICAL ERROR"


# Author: Tobias Manske <tobias.manske@mailbox.org>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
