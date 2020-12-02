# -*- coding: utf-8 -*-

import re


def asbool(val):
    """Converts a value into a boolean

    :param val: value to convert; accepts a wide range of
        possible representations, such as yes, no, true, false, on, off

    :return: True of val maps to true, False otherwise
    :rtype: boolean
    """
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    val = str(val).strip().lower()
    return val in ("t", "true", "y", "yes", "on", "1")


def asint(val, minimum=None, maximum=None):
    """Converts a value into an integer

    :param val: value to convert
    :param minimum: if specified, this determines the lower
        boundary for the returned value, defaults to None
    :param maximum: if specified, this determines the upper
        boundary for the returned value, defaults to None

    :return: integer representation of value
    :rtype: integer
    """
    if val is None:
        val = 0
    val = int(val)
    val = min(val, maximum if maximum else val)
    val = max(val, minimum if minimum else val)
    return val


def aslist(val):
    """Converts a comma-separated value string into a list

    :param val: value to convert, either a single value or a comma-separated string

    :return: list representation of the value passed in
    :rtype: list of strings
    """
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return str(val).replace(" ", "").split(",")


__UNITS = {"metric": "C", "kelvin": "K", "imperial": "F", "default": "C"}


def astemperature(val, unit="metric"):
    """Returns a temperature representation of the input value

    :param val: value to format, must be convertible into an integer
    :param unit: unit of the input value, supported units are:
        metric, kelvin, imperial, defaults to metric

    :return: temperature representation of the input value
    :rtype: string
    """
    return "{}°{}".format(int(val), __UNITS.get(unit.lower(), __UNITS["default"]))


def byte(val, fmt="{:.2f}", sys="IEC"):
    """Returns a byte representation of the input value

    :param val: value to format, must be convertible into a float
    :param fmt: optional output format string, defaults to {:.2f}
    :param sys: optional unit system specifier - SI (kilo, Mega, Giga, ...) or
        IEC (kibi, Mebi, Gibi, ...) - defaults to IEC

    :return: byte representation (e.g. <X> KiB, GiB, etc.) of the input value
    :rtype: string
    """

    if sys == "IEC":
        div = 1024.0
        units = ["", "Ki", "Mi", "Gi", "Ti"]
        final = "TiB"
    elif sys == "SI":
        div = 1000.0
        units = ["", "K", "M", "G", "T"]
        final = "TB"

    val = float(val)
    for unit in units:
        if val < div:
            return "{}{}B".format(fmt, unit).format(val)
        val /= div
    return "{}{}".format(fmt).format(val * div, final)


__seconds_pattern = re.compile(r"(([\d\.?]+)h)?(([\d\.]+)m)?([\d\.]+)?s?")


def seconds(duration):
    """Returns a time duration (in seconds) representation of the input value

    :param duration: value to format (e.g. 5h30m2s)

    :return: duration in seconds of the input value
    :rtype: float
    """
    if isinstance(duration, int) or isinstance(duration, float):
        return float(duration)

    matches = __seconds_pattern.match(duration)
    result = 0.0
    if matches.group(2):
        result += float(matches.group(2)) * 3600  # hours
    if matches.group(4):
        result += float(matches.group(4)) * 60  # minutes
    if matches.group(5):
        result += float(matches.group(5))  # seconds

    return result


def duration(duration, compact=False, unit=False):
    """Returns a time duration string representing the input value

    :param duration: value to format, must be convertible into an into
    :param compact: whether to show also seconds, defaults to False
    :param unit: whether to display he unit, defaults to False

    :return: duration representation (e.g. 5:02s) of the input value
    :rtype: string
    """
    duration = int(duration)
    if duration < 0:
        return "n/a"
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    suf = "m"
    res = "{:02d}:{:02d}".format(minutes, seconds)
    if hours > 0:
        if compact:
            res = "{:02d}:{:02d}".format(hours, minutes)
        else:
            res = "{:02d}:{}".format(hours, res)
        suf = "h"

    return "{}{}".format(res, suf if unit else "")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
