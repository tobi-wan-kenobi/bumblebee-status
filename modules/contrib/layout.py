# pylint: disable=C0111,R0903

"""Displays and changes the current keyboard layout

Requires the following executable:
    * setxkbmap
"""

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.current_layout)
        )
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd=self._next_keymap)
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE,
            cmd=self._prev_keymap)

    def _next_keymap(self, event):
        self._set_keymap(1)

    def _prev_keymap(self, event):
        self._set_keymap(-1)

    def _set_keymap(self, rotation):
        layouts = self.get_layouts()
        if len(layouts) == 1: return # nothing to do
        layouts = layouts[rotation:] + layouts[:rotation]

        layout_list = []
        variant_list = []
        for l in layouts:
            tmp = l.split(":")
            layout_list.append(tmp[0])
            variant_list.append(tmp[1] if len(tmp) > 1 else "")

        try:
            bumblebee.util.execute("setxkbmap -layout {} -variant {}".format(",".join(layout_list), ",".join(variant_list)))
        except RuntimeError:
            pass

    def get_layouts(self):
        try:
            res = bumblebee.util.execute("setxkbmap -query")
        except RuntimeError:
            return ["n/a"]
        layouts = []
        variants = []
        for line in res.split("\n"):
            if not line: continue
            if "layout" in line:
                layouts = line.split(":")[1].strip().split(",")
            if "variant" in line:
                variants = line.split(":")[1].strip().split(",")

        result = []
        for idx, layout in enumerate(layouts):
            if len(variants) > idx and variants[idx]:
                layout = "{}:{}".format(layout, variants[idx])
            result.append(layout)
        return result if len(result) > 0 else ["n/a"]

    def current_layout(self, widget):
        layouts = self.get_layouts()
        return layouts[0]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
