from __future__ import unicode_literals

import os
import sys
import json
import shlex
import threading
import subprocess
import bumblebee.output

def read_input(output):
    while True:
        line = sys.stdin.readline().strip(",").strip()
        if line == "[": continue
        if line == "]": break

        DEVNULL = open(os.devnull, 'wb')

        event = json.loads(line)
        cb = output.callback(event)
        if cb:
            cb(
                name=event.get("name", ""),
                instance=event.get("instance", ""),
                button=event.get("button", -1)
            )
        output.redraw()

class Output(bumblebee.output.Output):
    def __init__(self, args):
        super(Output, self).__init__(args)
        self._data = []

        self.add_callback("i3-msg workspace prev_on_output", 4)
        self.add_callback("i3-msg workspace next_on_output", 5)

        self._thread = threading.Thread(target=read_input, args=(self,))
        self._thread.start()

    def start(self):
        print(json.dumps({ "version": 1, "click_events": True }) + "[")

    def _draw(self, widgets, theme):
        for widget in widgets:
            if theme.separator(widget):
                self._data.append({
                    u"full_text": theme.separator(widget),
                    "color": theme.separator_color(widget),
                    "background": theme.separator_background(widget),
                    "separator": False,
                    "separator_block_width": 0,
                })

            self._data.append({
                u"full_text": " {} {} {} ".format(
                    theme.prefix(widget),
                    widget.text(),
                    theme.suffix(widget)
                ),
                "color": theme.color(widget),
                "background": theme.background(widget),
                "name": widget.module(),
                "instance": widget.instance(),
                "separator": theme.default_separators(widget),
                "separator_block_width": theme.separator_block_width(widget),
            })
            theme.next_widget()

    def flush(self):
        data = json.dumps(self._data)
        self._data = []
        print(data + ",")
        sys.stdout.flush()

    def stop(self):
        return "]"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
