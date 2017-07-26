# -*- coding: utf-8 -*-

import shlex
import datetime
import logging
import subprocess

try:
    from exceptions import RuntimeError
except ImportError:
    # Python3 doesn't require this anymore
    pass


def asbool(val):
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    val = str(val).strip().lower()
    return val in ("t", "true", "y", "yes", "on", "1")

def execute(cmd, wait=True):
    logging.info("executing command '{}'".format(cmd))
    args = shlex.split(cmd)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rv = None

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("{} exited with {}".format(cmd, proc.returncode))

        if hasattr(out, "decode"):
            rv = out.decode("utf-8")
        else:
            rv = out

    logging.info(u"command returned '{}'".format("" if not rv else rv))
    return rv

def bytefmt(num):
    for unit in [ "", "Ki", "Mi", "Gi" ]:
        if num < 1024.0:
            return "{:.2f}{}B".format(num, unit)
        num /= 1024.0
    return "{:.2f}GiB".format(num*1024.0)

def durationfmt(duration, shorten=False, suffix=False):
    duration = int(duration)
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    suf = "m"
    res = "{:02d}:{:02d}".format(minutes, seconds)
    if hours > 0:
        if shorten:
            res = "{:02d}:{:02d}".format(hours, minutes)
        else:
            res = "{:02d}:{}".format(hours, res)
        suf = "h"

    return "{}{}".format(res, suf if suffix else "")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
