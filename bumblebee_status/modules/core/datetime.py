# pylint: disable=C0111,R0903

"""Displays the current date and time.

Parameters:
    * datetime.format: strftime()-compatible formatting string
    * datetime.locale: locale to use rather than the system default
"""

from __future__ import absolute_import
import datetime
import locale

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd="calendar")
        l = locale.getdefaultlocale()
        if not l or l == (None, None):
            l = ("en_US", "UTF-8")
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_TIME, lcl.split("."))
        except Exception as e:
            locale.setlocale(locale.LC_TIME, ("en_US", "UTF-8"))

    def default_format(self):
        return "%x %X"

    def full_text(self, widget):
        enc = locale.getpreferredencoding()
        fmt = self.parameter("format", self.default_format())
        retval = datetime.datetime.now().strftime(fmt)
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
