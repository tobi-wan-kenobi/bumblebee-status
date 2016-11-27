import subprocess
import shlex
import bumblebee.module
import bumblebee.util

def description():
    return "Showws current keyboard layout and change it on click."

def parameters():
    return  [
        "layout.lang: pipe-separated list of languages to cycle through (e.g. us|rs|de). Default: en"
    ]


class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)

        self._languages = self._config.parameter("lang", "en").split("|")
        self._idx = 0

        output.add_callback(module=self.instance(), button=1, cmd=self.next_keymap)
        output.add_callback(module=self.instance(), button=3, cmd=self.prev_keymap)

    def next_keymap(self, event, widget):
        self._idx = self._idx + 1 if self._idx < len(self._languages) - 1 else 0
        self.set_keymap()

    def prev_keymap(self, event, widget):
        self._idx = self._idx - 1 if self._idx > 0 else len(self._languages) - 1
        self.set_keymap()

    def set_keymap(self):
        tmp = self._languages[self._idx].split(":")
        layout = tmp[0]
        variant = ""
        if len(tmp) > 1:
            variant = "-variant {}".format(tmp[1])
        bumblebee.util.execute("setxkbmap -layout {} {}".format(layout, variant))

    def widgets(self):
        lang = self._languages[self._idx]
        return bumblebee.output.Widget(self, lang)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
