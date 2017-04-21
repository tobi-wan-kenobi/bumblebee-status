import netifaces
import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = [
            bumblebee.output.Widget(name="traffic.down"),
            bumblebee.output.Widget(name="traffic.up"),
        ]
        super(Module, self).__init__(engine, config, widgets)
        self._exclude = tuple(filter(len, self.parameter("exclude", "lo,virbr,docker,vboxnet,veth").split(",")))
        self._update_widgets(widgets)
        self._status = None

    def state(self, widget):
        if widget.name == "traffic.down":
            return "down"
        if widget.name == "traffic.up":
            return "up"
        return self._status

    def update(self, widgets):
        self._update_widgets(widgets)

    def _update_widgets(self, widgets):
        _ifconfdata = bumblebee.util.execute('ifconfig')
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]

        interface = interfaces[0]
        if interface is '':
            interface = 'lo'

        _block = re.compile(r"" + interface + ":(.*\n)*", re.MULTILINE)
        _down = re.compile(r"RX packets .*  bytes (.*) \(", re.MULTILINE)
        _current_down = re.search(_down,re.search(_block,_ifconfdata).group(0)).group(1)
        _up = re.compile(r"TX packets .*  bytes (.*) \(", re.MULTILINE)
        _current_up = re.search(_up,re.search(_block,_ifconfdata).group(0)).group(1)

        widget_down = self.widget("traffic.down")
        widget_up = self.widget("traffic.up")
        if not widget_down:
            widget_down = bumblebee.output.Widget(name="traffic.down")
            widgets.append(widget_down)
        if not widget_up:
            widget_up = bumblebee.output.Widget(name="traffic.down")
            widgets.append(widget_up)

        _prev_down = widget_down.get("absdown", 0)
        _speed_down = bumblebee.util.bytefmt(int(_current_down) - int(_prev_down))
        widget_down.full_text("{}".format(_speed_down))
        widget_down.set("absdown", _current_down)

        _prev_up = widget_up.get("absup", 0)
        _speed_up = bumblebee.util.bytefmt(int(_current_up) - int(_prev_up))
        widget_up.full_text("{}".format(_speed_up))
        widget_up.set("absup", _current_up)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
