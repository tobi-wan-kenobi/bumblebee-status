# pylint: disable=C0111,R0903

"""Displays the current date and time in Persian(Jalali) Calendar.

Requires the following python packages:
    * jdatetime

Parameters:
    * datetime.format: strftime()-compatible formatting string. default: "%A %d %B" e.g., "جمعه ۱۳ اسفند"
    * datetime.locale: locale to use. default: "fa_IR"
"""

from __future__ import absolute_import
import jdatetime
import locale

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))

        l = ("fa_IR", "UTF-8")
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_ALL, lcl.split("."))
        except Exception as e:
            locale.setlocale(locale.LC_ALL, ("fa_IR", "UTF-8"))

    def default_format(self):
        return "%A %d %B"

    def full_text(self, widget):
        enc = locale.getpreferredencoding()
        fmt = self.parameter("format", self.default_format())
        retval = jdatetime.datetime.now().strftime(fmt)
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
