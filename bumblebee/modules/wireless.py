# pylint: disable=C0111,R0903


"""
Displays current status of the wireless card

Requires: https://github.com/joshvillbrandt/wireless

"""

import wireless

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
        def __init__(self, engine, config):
            super(Module, self).__init__(engine, config,
                                         bumblebee.output.Widget(full_text=self.wifistate))
            self._wifistate = "Not Connected"

        def wifistate(self, widget):
            return self._wifistate

        def update(self, widget):
            status = wireless.Wireless().current()
            if status == None:
                self._wifistate = "Not Connected"
            else:
                self._wifistate = status
        def state(self,widget):
            if self._wifistate == "Not Connected":
                return ["warning","Not Connected"]
            return ["connected"]
