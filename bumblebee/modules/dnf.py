import time
import shlex
import threading
import subprocess

import bumblebee.module
import bumblebee.util

def get_dnf_info(obj):
    while True:
        try:
            res = subprocess.check_output(shlex.split("dnf updateinfo"))
        except Exception as e:
            break

        security = 0
        bugfixes = 0
        enhancements = 0
        other = 0
        for line in res.split("\n"):
            if "expiration" in line: continue
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

        time.sleep(obj.interval())
    

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)
        self._interval = args[0] if args else 30*60
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
        for t in [ "security", "bugfix", "enhancement", "other" ]:
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
