# pylint: disable=C0111,R0903

"""Display HTTP status code

Parameters:
    * http__status.label: Prefix label (optional)
    * http__status.target: Target to retrieve the HTTP status from
    * http__status.expect: Expected HTTP status

contributed by `valkheim <https://github.com/valkheim>`_ - many thanks!
"""

from requests import head

import psutil

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    UNK = "UNK"

    @core.decorators.every(seconds=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.output))

        self.__label = self.parameter("label")
        self.__target = self.parameter("target")
        self.__expect = self.parameter("expect", "200")

    def labelize(self, s):
        if self.__label is None:
            return s
        return "{}: {}".format(self.__label, s)

    def getStatus(self):
        try:
            res = head(self.__target)
        except Exception as e:
            print(e)
            return self.UNK
        else:
            status = str(res.status_code)
            return status

    def getOutput(self):
        if self.__status == self.__expect:
            return self.labelize(self.__status)
        else:
            reason = " != {}".format(self.__expect)
            return self.labelize("{}{}".format(self.__status, reason))

    def output(self, widget):
        return self.__output

    def update(self):
        self.__status = self.getStatus()
        self.__output = self.getOutput()

    def state(self, widget):
        if self.__status == self.UNK:
            return "warning"
        if self.__status != self.__expect:
            return "critical"
        return self.__output


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
