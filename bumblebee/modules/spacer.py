import bumblebee.module
import bumblebee.util

def description():
    return "Draws a widget with configurable content."

def parameters():
    return [ "spacer.text: Text to draw (defaults to '')" ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config, alias):
        super(Module, self).__init__(output, config, alias)

    def widgets(self):
        return bumblebee.output.Widget(self, self._config.parameter("text", ""))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
