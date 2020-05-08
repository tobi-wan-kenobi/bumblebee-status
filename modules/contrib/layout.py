# pylint: disable=C0111,R0903

"""Displays and changes the current keyboard layout

Requires the following executable:
    * setxkbmap

contributed by `Pseudonick47 <https://github.com/Pseudonick47>`_ - many thanks!
"""

import core.module
import core.widget
import core.input

import util.cli


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.current_layout))

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__next_keymap)
        core.input.register(self, button=core.input.RIGHT_MOUSE, cmd=self.__prev_keymap)

    def __next_keymap(self, event):
        self._set_keymap(1)

    def __prev_keymap(self, event):
        self._set_keymap(-1)

    def _set_keymap(self, rotation):
        layouts = self.get_layouts()
        if len(layouts) == 1:
            return  # nothing to do
        layouts = layouts[rotation:] + layouts[:rotation]

        layout_list = []
        variant_list = []
        for l in layouts:
            tmp = l.split(":")
            layout_list.append(tmp[0])
            variant_list.append(tmp[1] if len(tmp) > 1 else "")

        util.cli.execute(
            "setxkbmap -layout {} -variant {}".format(
                ",".join(layout_list), ",".join(variant_list)
            ),
            ignore_errors=True,
        )

    def get_layouts(self):
        try:
            res = util.cli.execute("setxkbmap -query")
        except RuntimeError:
            return ["n/a"]
        layouts = []
        variants = []
        for line in res.split("\n"):
            if not line:
                continue
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
