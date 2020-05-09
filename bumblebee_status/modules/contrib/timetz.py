# pylint: disable=C0111,R0903

"""Displays the current date and time.

Parameters:
    * time.format: strftime()-compatible formatting string
    * time.locale: locale to use rather than the system default
"""

import core.decorators
from .datetimetz import Module


class Module(Module):
    @core.decorators.every(seconds=59)  # ensures one update per minute
    def __init__(self, config, theme):
        super().__init__(config, theme)

    def default_format(self):
        return "%X %Z"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
