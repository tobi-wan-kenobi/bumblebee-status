# pylint: disable=C0111,R0903

"""Print the branch and git status for the
currently focused window.

Requires:
    * xcwd
    * Python module 'pygit2'
"""

import os
import string
import pygit2

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.gitinfo)
        )
        self._fmt = self.parameter("format", "{branch} - {directory}")

    def gitinfo(self, widget):
        info = ""
        directory = None
        data = {
            "branch": "n/a",
        }
        try:
            directory = bumblebee.util.execute("xcwd").strip()
            directory = self._get_git_root(directory)
            repo = pygit2.Repository(directory)
            data["branch"] = repo.head.shorthand
            data["directory"] = directory
        except Exception as e:
            return e

        return string.Formatter().vformat(self._fmt, (), data)

    def _get_git_root(self, directory):
        while len(directory) > 1:
            if os.path.exists(os.path.join(directory, ".git")):
                return directory
            directory = "/".join(directory.split("/")[0:-1])
        return "/" 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
