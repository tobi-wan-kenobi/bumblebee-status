# pylint: disable=C0111,R0903

"""Print the branch and git status for the
currently focused window.

Requires:
    * xcwd
    * Python module 'pygit2'
"""

import os
import string
import logging
try:
    import pygit2
except ImportError:
    pass

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        super(Module, self).__init__(engine, config, widgets)
        self._engine = engine
        self._error = False
        self.update(self.widgets())

    def hidden(self):
        return self._error

    def update(self, widgets):
        state = {}
        new_widgets = []
        try:
            directory = bumblebee.util.execute("xcwd").strip()
            directory = self._get_git_root(directory)
            repo = pygit2.Repository(directory)

            new_widgets.append(bumblebee.output.Widget(name='git.main', full_text=repo.head.shorthand))

            for filepath, flags in repo.status().items():
                if flags == pygit2.GIT_STATUS_WT_NEW or \
                    flags == pygit2.GIT_STATUS_INDEX_NEW:
                    state['new'] = True
                if flags == pygit2.GIT_STATUS_WT_DELETED or \
                    flags == pygit2.GIT_STATUS_INDEX_DELETED:
                    state['deleted'] = True
                if flags == pygit2.GIT_STATUS_WT_MODIFIED or \
                    flags == pygit2.GIT_STATUS_INDEX_MODIFIED:
                    state['modified'] = True
            self._error = False
            if 'new' in state:
                new_widgets.append(bumblebee.output.Widget(name='git.new'))
            if 'modified' in state:
                new_widgets.append(bumblebee.output.Widget(name='git.modified'))
            if 'deleted' in state:
                new_widgets.append(bumblebee.output.Widget(name='git.deleted'))

            while len(widgets) > 0:
                del widgets[0]
            for widget in new_widgets:
                widgets.append(widget)
            
        except Exception as e:
            self._error = True

    def state(self, widget):
        return widget.name.split('.')[1]

    def _get_git_root(self, directory):
        while len(directory) > 1:
            if os.path.exists(os.path.join(directory, ".git")):
                return directory
            directory = "/".join(directory.split("/")[0:-1])
        return "/" 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
