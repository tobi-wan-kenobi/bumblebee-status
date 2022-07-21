#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=C0111,R0903

"""Displays the state of a Space API endpoint
Space API is an API for hackspaces based on JSON. See spaceapi.io for
an example.

Requires the following libraries:
    * requests

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.format: Format string for the output

Format Strings:
    * Format strings are indicated by double %%
    * They represent a leaf in the JSON tree, layers separated by '.'
    * Boolean values can be overwritten by appending '%true%false'
      in the format string
    * Example: to reference 'open' in '{'state':{'open': true}}'
      you would write '%%state.open%%', if you also want
      to say 'Open/Closed' depending on the boolean you
      would write '%%state.open%Open%Closed%%'

contributed by `rad4day <https://github.com/rad4day>`_ - many thanks!
"""

import requests
import threading
import re
import json

import core.module
import core.widget
import core.input
import core.decorators


def formatStringBuilder(s, json):
    """
    Parses Format Strings
    Parameter:
        s -> format string
        json -> the spaceapi response object
    """
    identifiers = re.findall(r"%%.*?%%", s)
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


class Module(core.module.Module):
    @core.decorators.every(minutes=15)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.getState))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__forceReload)

        self.__data = {}
        self.__error = None
        self.__thread = None

        # The URL representing the api endpoint
        self.__url = self.parameter("url", default="http://club.entropia.de/spaceapi")
        self._format = self.parameter(
            "format", default=" %%space%%: %%state.open%Open%Closed%%"
        )

    def state(self, widget):
        try:
            if self.__error is not None:
                return ["critical"]
            elif self.__data["state.open"]:
                return ["warning"]
            else:
                return []
        except KeyError:
            return ["critical"]

    def update(self):
        if not self.__thread or self.__thread.is_alive() == False:
            self.__thread = threading.Thread(target=self.get_api_async, args=())
            self.__thread.start()

    def getState(self, widget):
        text = self._format
        if self.__error is not None:
            text = self.__error
        else:
            try:
                text = formatStringBuilder(self._format, self.__data)
            except KeyError:
                text = "KeyError"
        return text

    def get_api_async(self):
        try:
            with requests.get(self.__url, timeout=10) as request:
                # Can't implement error handling for python2.7 if I use
                # request.json() as it uses simplejson in newer versions
                self.__data = self.__flatten(json.loads(request.text))
                self.__error = None
        except requests.exceptions.Timeout:
            self.__error = "Timeout"
        except requests.exceptions.HTTPError:
            self.__error = "HTTP Error"
        except ValueError:
            self.__error = "Not a JSON response"
        core.event.trigger("update", [self.id], redraw_only=True)

    # left_mouse_button handler
    def __forceReload(self, event):
        if self.__thread:
            self.__thread.raise_exception()
        self.__error = "RELOADING"
        core.event.trigger("update", [self.id], redraw_only=True)

    # Flattens the JSON structure recursively, e.g. ['space']['open']
    # becomes ['space.open']
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
