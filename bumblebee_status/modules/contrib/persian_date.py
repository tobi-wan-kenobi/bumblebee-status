# pylint: disable=C0111,R0903

"""Displays the current date and time in Persian(Jalali) Calendar.

Requires the following python packages:
    * jdatetime

Parameters:
    * datetime.format: strftime()-compatible formatting string. default: "%A %d %B" e.g., "جمعه ۱۳ اسفند"
    * datetime.locale: locale to use. default: "fa_IR"
"""

import jdatetime

import core.decorators
from modules.core.datetime import Module as dtmodule


class Module(dtmodule):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, dtlibrary=jdatetime)

    def default_format(self):
        return "%A %d %B"

    def default_locale(self):
        return ("fa_IR", "UTF-8")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
