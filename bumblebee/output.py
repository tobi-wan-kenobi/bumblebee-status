# pylint: disable=R0201

"""Output classes"""

import sys
import json

class Widget(object):
    """Represents a single visible block in the status bar"""
    def __init__(self, full_text):
        self._full_text = full_text

    def full_text(self):
        """Retrieve the full text to display in the widget"""
        if callable(self._full_text):
            return self._full_text()
        else:
            return self._full_text

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

    def draw(self, widgets, engine=None):
        """Draw a number of widgets"""
        if not isinstance(widgets, list):
            widgets = [widgets]
        result = []
        for widget in widgets:
            result.append({
                u"full_text": widget.full_text()
            })
        sys.stdout.write(json.dumps(result))

    def flush(self):
        """Flushes output"""
        sys.stdout.write(",\n")
        sys.stdout.flush()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
