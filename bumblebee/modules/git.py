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
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.gitinfo)
        )
        self._engine = engine
        self._fmt = self.parameter("format", "{branch} {flags}")
        self._error = False

    def hidden(self):
        return self._error

    def gitinfo(self, widget):
        info = ""
        directory = None
        data = {
            "branch": "n/a",
            "directory": "n/a",
            "flags": {},
        }
        try:
            directory = bumblebee.util.execute("xcwd").strip()
            directory = self._get_git_root(directory)
            repo = pygit2.Repository(directory)

            for filepath, flags in repo.status().items():
                if flags == pygit2.GIT_STATUS_WT_NEW or \
                    flags == pygit2.GIT_STATUS_INDEX_NEW:
                    data["flags"]["new"] = True
                if flags == pygit2.GIT_STATUS_WT_DELETED or \
                    flags == pygit2.GIT_STATUS_INDEX_DELETED:
                    data["flags"]["deleted"] = True
                if flags == pygit2.GIT_STATUS_WT_MODIFIED or \
                    flags == pygit2.GIT_STATUS_INDEX_MODIFIED:
                    data["flags"]["modified"] = True

            data["branch"] = repo.head.shorthand
            data["directory"] = directory
            data["flags"] = " ".join([self._engine._theme.symbol(widget, name, name[0]) for name in data["flags"].keys()])
            self._error = False
        except Exception as e:
            self._error = True
            logging.error(e)
            return "n/a"

        return string.Formatter().vformat(self._fmt, (), data)

    def _get_git_root(self, directory):
        while len(directory) > 1:
            if os.path.exists(os.path.join(directory, ".git")):
                return directory
            directory = "/".join(directory.split("/")[0:-1])
        return "/" 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
