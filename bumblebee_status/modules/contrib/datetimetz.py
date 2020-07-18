# pylint: disable=C0111,R0903

"""Displays the current date and time with timezone options.

Requires the following python packages:
    * tzlocal
    * pytz

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

contributed by `frankzhao <https://github.com/frankzhao>`_ - many thanks!
"""

from __future__ import absolute_import
import datetime
import locale
import logging
import pytz
import tzlocal

import core.module
import core.widget
import core.input

import util.format


def default_format(module):
    default = "%x %X %Z"
    if module == "datetz":
        default = "%x %Z"
    if module == "timetz":
        default = "%X %Z"
    return default


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.get_time))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.next_tz)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.prev_tz)
        self.__fmt = self.parameter("format", self.default_format())

        default_timezone = ""
        try:
            default_timezone = tzlocal.get_localzone().zone
        except Exception as e:
            logging.error("unable to get default timezone: {}".format(str(e)))
        try:
            self._timezones = util.format.aslist(
                self.parameter("timezone", default_timezone)
            )
        except:
            self._timezones = [default_timezone]
        self._current_tz = 0

        l = locale.getdefaultlocale()
        if not l or l == (None, None):
            l = ("en_US", "UTF-8")
        lcl = self.parameter("locale", ".".join(l))
        try:
            locale.setlocale(locale.LC_TIME, lcl.split("."))
        except Exception:
            locale.setlocale(locale.LC_TIME, ("en_US", "UTF-8"))

    def default_format(self):
        return "%x %X %Z"

    def get_time(self, widget):
        try:
            try:
                tz = pytz.timezone(self._timezones[self._current_tz].strip())
                retval = (
                    datetime.datetime.now(tz=tzlocal.get_localzone())
                    .astimezone(tz)
                    .strftime(self.__fmt)
                )
            except pytz.exceptions.UnknownTimeZoneError:
                retval = "[Unknown timezone: {}]".format(
                    self._timezones[self._current_tz].strip()
                )
        except Exception as e:
            logging.error("unable to get time: {}".format(str(e)))
            retval = "[n/a]"

        enc = locale.getpreferredencoding()
        if hasattr(retval, "decode"):
            return retval.decode(enc)
        return retval

    def next_tz(self, event):
        next_timezone = self._current_tz + 1
        if next_timezone >= len(self._timezones):
            next_timezone = 0  # wraparound
        self._current_tz = next_timezone

    def prev_tz(self, event):
        previous_timezone = self._current_tz - 1
        if previous_timezone < 0:
            previous_timezone = 0  # wraparound
        self._current_tz = previous_timezone


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
