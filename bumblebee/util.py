# -*- coding: utf-8 -*-

import shlex
import logging
import subprocess
import os

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

def aslist(val):
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return str(val).replace(' ', '').split(',')

def execute(cmd, wait=True):
    logging.info("executing command '{}'".format(cmd))
    args = shlex.split(cmd)
    my_env = os.environ.copy()
    my_env['LC_ALL'] = "C"
    proc = subprocess.Popen(args, env=my_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    rv = None

    if wait:
        out, _ = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError("{} exited with {}".format(cmd, proc.returncode))

        if hasattr(out, "decode"):
            rv = out.decode("utf-8", "ignore")
        else:
            rv = out

    logging.info(u"command returned '{}'".format("" if not rv else rv))
    return rv

def bytefmt(num, fmt="{:.2f}"):
    """
        format a value of bytes to a more human readable pattern
        example: 15 * 1024 becomes 15KiB

        Args:

            num (int): bytes

            fmt (string): format

        Return: string
    """
    for unit in ["", "Ki", "Mi", "Gi"]:
        if num < 1024.0:
            return "{}{}B".format(fmt, unit).format(num)
        num /= 1024.0
    return "{}GiB".format(fmt).format(num*1024.0)

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

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        localPATH = os.environ["PATH"].split(os.pathsep)
        localPATH += ["/sbin", "/usr/sbin/", "/usr/local/sbin"]
        for path in localPATH:
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
