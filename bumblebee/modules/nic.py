import netifaces
import bumblebee.module

def description():
    return "Displays the names, IP addresses and status of each available interface."

def parameters():
    return [
            "nic.exclude: Comma-separated list of interface prefixes to exlude (defaults to: \"lo,virbr,docker,vboxnet,veth\")"
    ]

class Module(bumblebee.module.Module):
    def __init__(self, output, config):
        super(Module, self).__init__(output, config)
        self._exclude = tuple(filter(len, self._config.parameter("exclude", "lo,virbr,docker,vboxnet,veth").split(",")))
        self._state = "down"
        self._typecache = {}

    def widgets(self):
        result = []
        interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]
        for intf in interfaces:
            addr = []
            state = "down"
            try:
                if netifaces.AF_INET in netifaces.ifaddresses(intf):
                    for ip in netifaces.ifaddresses(intf)[netifaces.AF_INET]:
                        if "addr" in ip and ip["addr"] != "":
                            addr.append(ip["addr"])
                            state = "up"
            except Exception as e:
                addr = []
            widget = bumblebee.output.Widget(self, "{} {} {}".format(
                intf, state, ", ".join(addr)
            ))
            widget.set("intf", intf)
            widget.set("state", state)
            result.append(widget)

        return result

    def _iswlan(self, intf):
        # wifi, wlan, wlp, seems to work for me
        if intf.startswith("w"): return True
        return False

    def _istunnel(self, intf):
        return intf.startswith("tun")

    def state(self, widget):
        intf = widget.get("intf")

        if not intf in self._typecache:
            t = "wireless" if self._iswlan(intf) else "wired"
            t = "tunnel" if self._istunnel(intf) else t
            self._typecache[intf] = t

        return "{}-{}".format(self._typecache[intf], widget.get("state"))

    def warning(self, widget):
        return widget.get("state") != "up"

    def critical(self, widget):
        return widget.get("state") == "down"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
