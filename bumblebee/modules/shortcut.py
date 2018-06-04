# pylint: disable=C0112,R0903

"""Shows a widget per user-defined shortcut and allows to define the behaviour
when clicking on it.

For more than one shortcut, the commands and labels are strings separated by
a demiliter (; semicolon by default).

For example in order to create two shortcuts labeled A and B with commands
cmdA and cmdB you could do:

 ./bumblebee-status -m shortcut -p shortcut.cmd="ls;ps" shortcut.label="A;B"

Parameters:
    * shortcut.cmds  : List of commands to execute
    * shortcut.labels: List of widgets' labels (text)
    * shortcut.delim : Commands and labels delimiter (; semicolon by default)
"""

import logging
import bumblebee.engine
import bumblebee.output
import bumblebee.input

LINK = "https://github.com/tobi-wan-kenobi/bumblebee-status/wiki"
LABEL = "Click me"

class Module(bumblebee.engine.Module):
    """ Shortcut module."""

    def __init__(self, engine, config):
        widgets = []
        self._engine = engine
        super(Module, self).__init__(engine, config, widgets)

        self._labels = self.parameter("labels", "{}".format(LABEL))
        self._cmds = self.parameter("cmds", "firefox {}".format(LINK))
        self._delim = self.parameter("delim", ";")

        self.update_widgets(widgets)

    def update_widgets(self, widgets):
        """ Creates a set of widget per user define shortcut."""

        cmds = self._cmds.split(self._delim)
        labels = self._labels.split(self._delim)

        # to be on the safe side create as many widgets as there are data (cmds or labels)
        num_shortcuts = min(len(cmds), len(labels))

        # report possible problem as a warning
        if len(cmds) is not len(labels):
            logging.warning("shortcut: the number of commands does not match "\
                            "the number of provided labels.")
            logging.warning("cmds : %s, labels : %s", cmds, labels)

        for idx in range(0, num_shortcuts):
            cmd = cmds[idx]
            label = labels[idx]

            widget = bumblebee.output.Widget(full_text=label)
            self._engine.input.register_callback(widget, button=bumblebee.input.LEFT_MOUSE, cmd=cmd)

            widgets.append(widget)

    def update(self, widgets):
        if len(widgets) <= 0:
            self.update_widgets(widgets)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
