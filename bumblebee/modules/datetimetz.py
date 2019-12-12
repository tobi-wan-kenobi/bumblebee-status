# pylint: disable=C0111,R0903

"""Displays the current date and time with timezone options.

Parameters:
    * datetimetz.format   : strftime()-compatible formatting string
    * datetimetz.timezone : IANA timezone name
    * datetz.format       : alias for datetimetz.format
    * timetz.format       : alias for datetimetz.format
    * timetz.timezone     : alias for datetimetz.timezone
    * datetimetz.locale   : locale to use rather than the system default
    * datetz.locale       : alias for datetimetz.locale
    * timetz.locale       : alias for datetimetz.locale
    * timetz.timezone     : alias for datetimetz.timezone
"""

from __future__ import absolute_import
import datetime
import locale
import logging
try:
    import pytz
    import tzlocal
except:
    pass
import bumblebee.input
import bumblebee.output
import bumblebee.engine

def default_format(module):
    default = "%x %X %Z"
    if module == "datetz":
        default = "%x %Z"
    if module == "timetz":
        default = "%X %Z"
    return default

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.get_time))
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self.next_tz)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=self.prev_tz)
        self._fmt = self.parameter("format", default_format(self.name))
        default_timezone = ""
        try:
            default_timezone = tzlocal.get_localzone().zone
        except Exception as e:
            logging.error('unable to get default timezone: {}'.format(str(e)))
        try:
            self._timezones = self.parameter("timezone", default_timezone).split(",")
        except:
            self._timezones = [default_timezone]
        self._current_tz = 0

        l = locale.getdefaultlocale()
        if not l or l == (None, None):
            l = ('en_US', 'UTF-8')
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_TIME, lcl.split("."))
        except Exception:
            locale.setlocale(locale.LC_TIME, ('en_US', 'UTF-8'))

    def get_time(self, widget):
        try:
            try:
                tz = pytz.timezone(self._timezones[self._current_tz].strip())
                retval = datetime.datetime.now(tz=tzlocal.get_localzone()).astimezone(tz).strftime(self._fmt)
            except pytz.exceptions.UnknownTimeZoneError:
                retval = "[Unknown timezone: {}]".format(self._timezones[self._current_tz].strip())
        except Exception as e:
            logging.error('unable to get time: {}'.format(str(e)))
            retval = "[n/a]"

        enc = locale.getpreferredencoding()
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval

    def next_tz(self, event):
        next_timezone = self._current_tz + 1
        if next_timezone >= len(self._timezones):
            next_timezone = 0     # wraparound
        self._current_tz = next_timezone

    def prev_tz(self, event):
        previous_timezone = self._current_tz - 1
        if previous_timezone < 0:
            previous_timezone = 0     # wraparound
        self._current_tz = previous_timezone

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
