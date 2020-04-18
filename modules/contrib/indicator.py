#pylint: disable=C0111,R0903

"""Displays the indicator status, for numlock, scrolllock and capslock 

Parameters:
    * indicator.include: Comma-separated list of interface prefixes to include (defaults to "numlock,capslock")
    * indicator.signalstype: If you want the signali type color to be "critical" or "warning" (defaults to "warning")
"""


import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        self.status = False
        super(Module,self).__init__(engine, config, widgets)
        self._include = tuple(filter(len, self.parameter("include", "NumLock,CapsLock").split(",")))
        self._signalType = self.parameter("signaltype") if not self.parameter("signaltype") is None else "warning"

    def update(self, widgets):
        self._update_widgets(widgets)

    def state(self, widget):
        states = []
        if widget.status:
            states.append(self._signalType)
        elif not widget.status:
            states.append("normal")
        return states

    def _update_widgets(self, widgets):
        status_line = "" 
        for line in bumblebee.util.execute("xset q").replace(" ", "").split("\n"):
            if "capslock" in line.lower():
                status_line = line  
                break
            
        for indicator in self._include:
            widget = self.widget(indicator)
            if not widget:
                widget = bumblebee.output.Widget(name=indicator)
                widgets.append(widget)

            widget.status = True if indicator.lower()+":on" in status_line.lower() else False
            widget.full_text(indicator)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
