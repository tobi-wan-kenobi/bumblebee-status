from __future__ import absolute_import

import re
import time
import shlex
import threading
import subprocess

import bumblebee.module
import bumblebee.util

def description():
    return "Periodically checks the RTT of a configurable IP"

def parameters():
    return [
        "ping.interval: Time in seconds between two RTT checks (defaults to 60)",
        "ping.address: IP address to check",
        "ping.warning: Threshold for warning state, in seconds (defaults to 1.0)",
        "ping.critical: Threshold for critical state, in seconds (defaults to 2.0)",
        "ping.timeout: Timeout for waiting for a reply (defaults to 5.0)",
        "ping.probes: Number of probes to send (defaults to 5)",
    ]

def get_rtt(obj):
    loops = obj.get("interval")

    for thread in threading.enumerate():
        if thread.name == "MainThread":
            main = thread

    interval = obj.get("interval")
    while main.is_alive():
        loops += 1
        if loops < interval:
            time.sleep(1)
            continue

        loops = 0
        try:
            res = subprocess.check_output(shlex.split("ping -n -q -c {} -W {} {}".format(
                obj.get("rtt-probes"), obj.get("rtt-timeout"), obj.get("address")
            )))
            obj.set("rtt-unreachable", False)

            for line in res.decode().split("\n"):
                if not line.startswith("rtt"): continue
                m = re.search(r'([0-9\.]+)/([0-9\.]+)/([0-9\.]+)/([0-9\.]+)\s+(\S+)', line)

                obj.set("rtt-min", float(m.group(1)))
                obj.set("rtt-avg", float(m.group(2)))
                obj.set("rtt-max", float(m.group(3)))
                obj.set("rtt-unit", m.group(5))
        except Exception as e:
            obj.set("rtt-unreachable", True)


class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)

        self._counter = {}

        self.set("address", self._config.parameter("address", "8.8.8.8"))
        self.set("interval", self._config.parameter("interval", 60))
        self.set("rtt-probes", self._config.parameter("probes", 5))
        self.set("rtt-timeout", self._config.parameter("timeout", 5.0))

        self._thread = threading.Thread(target=get_rtt, args=(self,))
        self._thread.start()

    def set(self, what, value):
        self._counter[what] = value

    def get(self, what):
        return self._counter.get(what, 0)

    def widgets(self):
        text = "{}: {:.1f}{}".format(
            self.get("address"),
            self.get("rtt-avg"),
            self.get("rtt-unit")
        )

        if self.get("rtt-unreachable"):
            text = "{}: unreachable".format(self.get("address"))

        return bumblebee.output.Widget(self, text)

    def warning(self, widget):
        return self.get("rtt-avg") > float(self._config.parameter("warning", 1.0))*1000.0

    def critical(self, widget):
        if self.get("rtt-unreachable"): return True
        return self.get("rtt-avg") > float(self._config.parameter("critical", 2.0))*1000.0

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
