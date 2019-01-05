# pylint: disable=C0111,R0903

"""Displays the state of a spaceapi endpoint

Requires the following libraries:
    * requests
    * regex

Parameters:
    * spaceapi.url: String representation of the api endpoint
    * spaceapi.format: Format string for the output (refer to code)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import requests
import threading
import re
from json.decoder import JSONDecodeError


def formatStringBuilder(s: str, json: dict) -> str:
    """
    This function seems to be in dire need of some explanation so here it is:
        It basically searches the format string for strings of the pattern
        %%ITEM.IN.TREE[%IFTRUE%IFFALSE]%%. For example to query the state of
        the space you'd write %%state.open%% as it's located in json[state][open]
        according to the API specificaion. As the output of true or false doesn't
        look to great you can specify the text you want to have shown so you'd
        write %%state.open%Open%Closed%% to overwrite true/false with Open/Closed.
    """
    identifiers = re.findall("%%.*?%%", s)
    for i in identifiers:
        ic = i[2:-2]  # Discard %%
        j = ic.split("%")

        if len(j) != 3 and len(j) != 1:
            return "INVALID SYNTAX"

        arr = j[0].split(".")
        repl = json
        for a in arr:  # Walk the JSON tree to find replacement
            repl = repl[a]

        if len(j) == 1:
            s = s.replace(i, repl)
        elif repl:
            s = s.replace(i, j[1])
        else:
            s = s.replace(i, j[2])
    return s


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
        self._format = self.parameter(
            "format", default=" %%space%%: %%state.open%Open%Closed%%"
        )

    def state(self, widget):
        try:
            if self._error is not None:
                return ["critical"]
            elif self._data["state"]["open"]:
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
                self._data = request.json()
                self._error = None
        except requests.exceptions.Timeout:
            self._error = "Timeout"
        except requests.exceptions.HTTPError:
            self._error = "HTTP Error"
        except JSONDecodeError:
            self._error = "Not a JSON response"


# Author: Tobias Manske <tobias@chaoswg.xyz>
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
