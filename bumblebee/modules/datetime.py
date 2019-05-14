# pylint: disable=C0111,R0903

"""Displays the current date and time.

Parameters:
    * datetime.format: strftime()-compatible formatting string
    * date.format    : alias for datetime.format
    * time.format    : alias for datetime.format
    * datetime.locale: locale to use rather than the system default
    * date.locale    : alias for datetime.locale
    * time.locale    : alias for datetime.locale
"""

from __future__ import absolute_import
import datetime
import locale
import bumblebee.engine

ALIASES = ["date", "time"]

def default_format(module):
    default = "%x %X"
    if module == "date":
        default = "%x"
    if module == "time":
        default = "%X"
    return default

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.get_time))
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                    cmd="calendar")
        self._fmt = self.parameter("format", default_format(self.name))
        l = locale.getdefaultlocale()
        if not l or l == (None, None):
            l = ('en_US', 'UTF-8')
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_TIME, lcl.split("."))
        except Exception as e:
            locale.setlocale(locale.LC_TIME, ('en_US', 'UTF-8'))

    def get_time(self, widget):
        enc = locale.getpreferredencoding()
        retval = datetime.datetime.now().strftime(self._fmt)
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
