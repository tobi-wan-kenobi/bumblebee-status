# pylint: disable=R0201

"""Output classes"""

import sys
import json

class I3BarOutput(object):
    """Manage output according to the i3bar protocol"""
    def __init__(self):
        pass

    def start(self):
        """Print start preamble for i3bar protocol"""
        sys.stdout.write(json.dumps({"version": 1, "click_events": True}) + "[\n")

    def stop(self):
        """Finish i3bar protocol"""
        sys.stdout.write("]\n")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
