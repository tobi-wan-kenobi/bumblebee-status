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
            cb = cb.format(
                name = event.get("name", ""),
                instance = event.get("instance", ""),
                button = event.get("button", -1)
            )
            subprocess.Popen(shlex.split(cb), stdout=DEVNULL, stderr=DEVNULL)

class i3bar(bumblebee.output.Output):
    def __init__(self, theme):
        super(i3bar, self).__init__(theme)
        self._data = []

        self.add_callback("i3-msg workspace prev_on_output", 4)
        self.add_callback("i3-msg workspace next_on_output", 5)

        self._thread = threading.Thread(target=read_input, args=(self,))
        self._thread.start()

    def start(self):
        return json.dumps({ "version": 1, "click_events": True }) + "["

    def add(self, obj):
        theme = self.theme()

        while True:
            d = obj.data()
            data = {
                u"full_text": "{}{}{}".format(theme.prefix(obj), d, theme.suffix(obj)),
                "color": theme.color(obj),
                "background": theme.background(obj),
                "name": obj.__module__.replace("bumblebee.modules.",""),
                "instance": obj.instance() if hasattr(obj, "instance") else None,
            }

            if theme.urgent(obj) and obj.critical():
                data["urgent"] = True

            if theme.default_separators(obj) == False:
                data["separator"] = False
                data["separator_block_width"] = 0
                if theme.separator(obj):
                    self._data.append({
                        u"full_text": theme.separator(obj),
                        "color": theme.background(obj),
                        "background": theme.previous_background(),
                        "separator": False,
                        "separator_block_width": 0,
                    })

            self._data.append(data)
            if obj.next() == False:
                break
            theme.next()

    def get(self):
        data = json.dumps(self._data)
        self._data = []
        return data + ","

    def stop(self):
        return "]"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
