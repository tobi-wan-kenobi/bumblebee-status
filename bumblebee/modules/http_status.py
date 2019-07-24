# pylint: disable=C0111,R0903

"""Display HTTP status code

Parameters:
    * http_status.label: Prefix label (optional)
    * http_status.target: Target to retrieve the HTTP status from
    * http_status.expect: Expected HTTP status
"""

from requests import head

import psutil
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    UNK = "UNK"

    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.output)
        super(Module, self).__init__(engine, config, widget)

        self._label = self.parameter("label")
        self._target = self.parameter("target")
        self._expect = self.parameter("expect", "200")
        self._status = self.getStatus()
        self._output = self.getOutput()

    def labelize(self, s):
        if self._label is None:
            return s
        return "{}: {}".format(self._label, s)

    def getStatus(self):
        try:
            res = head(self._target)
        except Exception:
            return self.UNK
        else:
            status = str(res.status_code)
            self._status = status
            return status

    def getOutput(self):
        if self._status == self._expect:
            return self.labelize(self._status)
        else:
            reason = " != {}".format(self._expect)
            return self.labelize("{}{}".format(self._status, reason))

    def output(self, widget):
        return self._output

    def update(self, widgets):
        self.getStatus()
        self._output = self.getOutput()

    def state(self, widget):
        if self._status == self.UNK:
            return "warning"
        if self._status != self._expect:
            return "critical"
        return self._output


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
