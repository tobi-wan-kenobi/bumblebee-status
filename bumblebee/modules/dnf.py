from __future__ import absolute_import

import time
import shlex
import threading
import subprocess

import bumblebee.module
import bumblebee.util

def usage():
    return "dnf or dnf::<interval in seconds, defaults to 3600>"

def notes():
    return "Spawns a separate thread that invokes 'dnf updateinfo' every <interval> seconds. Critical status is if there is either more than 50 updates pending, or at least one of them is a security update."

def description():
    return "Checks DNF for updated packages and displays the number of <security>/<bugfixes>/<enhancements>/<other> pending updates."

def get_dnf_info(obj):

    loops = 0

    for thread in threading.enumerate():
        if thread.name == "MainThread":
            main = thread

    while main.is_alive():
        try:
            res = subprocess.check_output(shlex.split("dnf updateinfo"))
        except Exception as e:
            break

        loops += 1
        time.sleep(1)
        if loops < obj.interval():
            continue

        loops = 0

        security = 0
        bugfixes = 0
        enhancements = 0
        other = 0
        for line in res.split("\n"):
            if "expiration" in line: continue
            if not line.startswith(" "): continue
            elif "ecurity" in line:
                for s in str.split(line):
                    if s.isdigit(): security += int(s)
            elif "ugfix" in line:
                for s in str.split(line):
                    if s.isdigit(): bugfixes += int(s)
            elif "hancement" in line:
                for s in str.split(line):
                    if s.isdigit(): enhancements += int(s)
            else:
                for s in str.split(line):
                    if s.isdigit(): other += int(s)

        obj.set("security", security)
        obj.set("bugfixes", bugfixes)
        obj.set("enhancements", enhancements)
        obj.set("other", other)

class Module(bumblebee.module.Module):
    def __init__(self, output, args):
        super(Module, self).__init__(args)

        self._interval = int(args[0]) if args else 30*60
        self._counter = {}
        self._thread = threading.Thread(target=get_dnf_info, args=(self,))
        self._thread.start()

    def interval(self):
        return self._interval

    def set(self, what, value):
        self._counter[what] = value

    def get(self, what):
        return self._counter.get(what, 0)

    def data(self):
        result = []
        for t in [ "security", "bugfixes", "enhancements", "other" ]:
            result.append(str(self.get(t)))

        return "/".join(result)

    def state(self):
        total = sum(self._counter.values())
        if total == 0: return "good"
        return "default"

    def warning(self):
        total = sum(self._counter.values())
        return total > 0

    def critical(self):
        total = sum(self._counter.values())
        return total > 50 or self._counter.get("security", 0) > 0

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
