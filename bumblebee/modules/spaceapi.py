#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0111,R0903

"""Displays the state of a Space API endpoint
Space API is an API for hackspaces based on JSON. See spaceapi.io for
an example.

Requires the following libraries:
    * requests
    * regex

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.format: Format string for the output

Format Strings:
    * Format strings are indicated by double %%
    * They represent a leaf in the JSON tree, layers seperated by "."
    * Boolean values can be overwritten by appending "%true%false"
      in the format string
    * Example: to reference "open" in "{"state":{"open": true}}"
               you would write "%%state.open%%", if you also want
               to say "Open/Closed" depending on the boolean you
               would write "%%state.open%Open%Closed%%"
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import requests
import threading
import re
import json


def formatStringBuilder(s, json):
    """
    Parses Format Strings
    Parameter:
        s -> format string
        json -> the spaceapi response object
    """
    identifiers = re.findall("%%.*?%%", s)
    for i in identifiers:
        ic = i[2:-2]  # Discard %%
        j = ic.split("%")

        # Only neither of, or both true AND false may be overwritten
        if len(j) != 3 and len(j) != 1:
            return "INVALID FORMAT STRING"

        if len(j) == 1:  # no overwrite
            s = s.replace(i, json[j[0]])
        elif json[j[0]]:  # overwrite for True
            s = s.replace(i, j[1])
        else:  # overwrite for False
            s = s.replace(i, j[2])
    return s


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(
            engine, config, bumblebee.output.Widget(full_text=self.getState)
        )

        engine.input.register_callback(
            self, button=bumblebee.input.LEFT_MOUSE, cmd=self.__forceReload
        )

        self._data = {}
        self._error = None

        self._threadingCount = 0

        # The URL representing the api endpoint
        self._url = self.parameter("url", default="http://club.entropia.de/spaceapi")
        self._format = self.parameter(
            "format", default=u" %%space%%: %%state.open%Open%Closed%%"
        )

    def state(self, widget):
        try:
            if self._error is not None:
                return ["critical"]
            elif self._data["state.open"]:
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
                text = formatStringBuilder(self._format, self._data)
            except KeyError:
                text = "KeyError"
        return text

    def get_api_async(self):
        try:
            with requests.get(self._url, timeout=10) as request:
                # Can't implement error handling for python2.7 if I use
                # request.json() as it uses simplejson in newer versions
                self._data = self.__flatten(json.loads(request.text))
                self._error = None
        except requests.exceptions.Timeout:
            self._error = "Timeout"
        except requests.exceptions.HTTPError:
            self._error = "HTTP Error"
        except ValueError:
            self._error = "Not a JSON response"

    # left_mouse_button handler
    def __forceReload(self, event):
        self._threadingCount += 300
        self._error = "RELOADING"

    # Flattens the JSON structure recursively, e.g. ["space"]["open"]
    # becomes ["space.open"]
    def __flatten(self, json):
        out = {}
        for key in json:
            value = json[key]
            if type(value) is dict:
                flattened_key = self.__flatten(value)
                for fk in flattened_key:
                    out[key + "." + fk] = flattened_key[fk]
            else:
                out[key] = value
        return out


# Author: Tobias Manske <tobias@chaoswg.xyz>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
