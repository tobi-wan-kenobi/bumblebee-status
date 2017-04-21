import netifaces
import re

import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = []
        super(Module, self).__init__(engine, config, widgets)
        self._exclude = tuple(filter(len, self.parameter("exclude", "lo,virbr,docker,vboxnet,veth").split(",")))
        self._update_widgets(widgets)

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

        widget = self.widget("traffic")
        if not widget:
            widget = bumblebee.output.Widget(name="traffic")
            widgets.append(widget)
        _prev_up = widget.get("absup", 0)
        _prev_down = widget.get("absdown", 0)
        _speed_down = bumblebee.util.bytefmt(int(_current_down) - int(_prev_down))
        _speed_up = bumblebee.util.bytefmt(int(_current_up) - int(_prev_up))
        widget.full_text("{} {} {}".format(interface, _speed_down, _speed_up))
        widget.set("absdown", _current_down)
        widget.set("absup", _current_up)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
