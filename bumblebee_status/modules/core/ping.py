# pylint: disable=C0111,R0903

"""Periodically checks the RTT of a configurable host using ICMP echos

Requires the following executable:
    * ping

Parameters:
    * ping.address : IP address to check
    * ping.timeout : Timeout for waiting for a reply (defaults to 5.0)
    * ping.probes  : Number of probes to send (defaults to 5)
    * ping.warning : Threshold for warning state, in seconds (defaults to 1.0)
    * ping.critical: Threshold for critical state, in seconds (defaults to 2.0)
"""

import re
import time

import core.module
import core.widget
import core.event
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(seconds=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.rtt))

        self.background = True

        widget = self.widget()

        widget.set("address", self.parameter("address", "8.8.8.8"))
        widget.set("rtt-probes", self.parameter("probes", 5))
        widget.set("rtt-timeout", self.parameter("timeout", 5.0))
        widget.set("rtt-avg", 0.0)
        widget.set("rtt-unit", "")
        widget.set("packet-loss", 0)

    def rtt(self, widget):
        if widget.get("rtt-unreachable"):
            return "{}: unreachable".format(widget.get("address"))
        return "{}: {:.1f}{} ({}%)".format(
            widget.get("address"),
            widget.get("rtt-avg"),
            widget.get("rtt-unit"),
            widget.get("packet-loss"),
        )

    def state(self, widget):
        if widget.get("rtt-unreachable"):
            return ["critical"]
        return self.threshold_state(widget.get("rtt-avg"), 1000.0, 2000.0)

    def update(self):
        widget = self.widget()
        try:
            widget.set("rtt-unreachable", False)
            res = util.cli.execute(
                "ping -n -q -c {} -W {} {}".format(
                    widget.get("rtt-probes"),
                    widget.get("rtt-timeout"),
                    widget.get("address"),
                )
            )

            for line in res.split("\n"):
                if line.startswith(
                    "{} packets transmitted".format(widget.get("rtt-probes"))
                ):
                    m = re.search(r"(\d+)% packet loss", line)

                    widget.set("packet-loss", m.group(1))

                if not line.startswith("rtt"):
                    continue
                m = re.search(r"([0-9\.]+)/([0-9\.]+)/([0-9\.]+)/([0-9\.]+)\s+(\S+)", line)

                widget.set("rtt-min", float(m.group(1)))
                widget.set("rtt-avg", float(m.group(2)))
                widget.set("rtt-max", float(m.group(3)))
                widget.set("rtt-unit", m.group(5))
        except Exception as e:
            widget.set("rtt-unreachable", True)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
