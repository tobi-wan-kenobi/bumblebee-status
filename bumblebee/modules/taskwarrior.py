"""Displays the number of pending tasks in TaskWarrior.

Requires the following library:
    * taskw

Parameters:
    * taskwarrior.taskrc : path to the taskrc file (defaults to ~/.taskrc)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

try:
    from taskw import TaskWarrior
except:
    pass


class Module(bumblebee.engine.Module):
    """TaskWarrior module."""

    def __init__(self, engine, config):
        """Initialize taskwarrior module."""
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(
                                         full_text=self.output))
        self._pending_tasks_count = "0"

    def update(self, widgets):
        """Return a string with the number of pending tasks from TaskWarrior."""
        try:
            taskrc = self.parameter("taskrc", "~/.taskrc")
            w = TaskWarrior(config_filename=taskrc)
            pending_tasks = w.filter_tasks({'status': 'pending'})
            self._pending_tasks_count = str(len(pending_tasks))
        except:
            self._pending_tasks_count = 'Error'

    def output(self, _):
        """Format the task counter to output in bumblebee."""
        return "{}".format(self._pending_tasks_count)
