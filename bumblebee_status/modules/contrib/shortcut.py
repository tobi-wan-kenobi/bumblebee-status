# pylint: disable=C0112,R0903

"""Shows a widget per user-defined shortcut and allows to define the behaviour
when clicking on it.

For more than one shortcut, the commands and labels are strings separated by
a delimiter (; semicolon by default).

For example in order to create two shortcuts labeled A and B with commands
cmdA and cmdB you could do:

 ./bumblebee-status -m shortcut -p shortcut.cmd='firefox https://www.google.com;google-chrome https://google.com' shortcut.label='Google (Firefox);Google (Chrome)'

Parameters:
    * shortcut.cmds  : List of commands to execute
    * shortcut.labels: List of widgets' labels (text)
    * shortcut.delim : Commands and labels delimiter (; semicolon by default)


contributed by `cacyss0807 <https://github.com/cacyss0807>`_ - many thanks!
"""

import logging

LINK = "https://github.com/tobi-wan-kenobi/bumblebee-status/wiki"
LABEL = "Click me"

import core.module
import core.input
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, [])

        self.__labels = self.parameter("labels", "{}".format(LABEL))
        self.__cmds = self.parameter("cmds", "firefox {}".format(LINK))
        self.__delim = self.parameter("delim", ";")

        self.update_widgets()

    def update_widgets(self):
        """ Creates a set of widget per user define shortcut."""

        cmds = self.__cmds.split(self.__delim)
        labels = self.__labels.split(self.__delim)

        # to be on the safe side create as many widgets as there are data (cmds or labels)
        num_shortcuts = min(len(cmds), len(labels))

        # report possible problem as a warning
        if len(cmds) is not len(labels):
            logging.warning(
                "shortcut: the number of commands does not match "
                "the number of provided labels."
            )
            logging.warning("cmds : %s, labels : %s", cmds, labels)

        for idx in range(0, num_shortcuts):
            cmd = cmds[idx]
            label = labels[idx]

            widget = self.add_widget(full_text=label)
            core.input.register(widget, button=core.input.LEFT_MOUSE, cmd=cmd)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
