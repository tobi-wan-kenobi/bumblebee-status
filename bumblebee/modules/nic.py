import pyroute2
import netifaces
import bumblebee.module

def usage():
    return "nic"

def notes():
    return "Interfaces starting with 'lo' or 'virbr' are ignored. Critical if the status of an interface is 'down', Warning if it is anything else but 'up'. Interface status is derived from whether an IP address is available or not."

def description():
    return "Displays the names, IP addresses and status of each available interface."

class Module(bumblebee.module.Module):
    def __init__(self, args):
        super(Module, self).__init__(args)
        self._exclude = ( "lo", "virbr" )
        self._interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]
        self._index = 0
        self._intf = self._interfaces[0] if len(self._interfaces) > 0 else None
        self._cache = {}
        self._state = "down"

    def data(self):
        if len(self._interfaces) <= self._index:
            return "n/a"
        self._intf = self._interfaces[self._index]
        self._state = "down"
        addr = []

        try:
            if netifaces.AF_INET in netifaces.ifaddresses(self._intf):
                for ip in netifaces.ifaddresses(self._intf)[netifaces.AF_INET]:
                    if "addr" in ip and ip["addr"] != "":
                        addr.append(ip["addr"])
                        self._state = "up"
        except Exception as e:
            self._state = "down"
            addr = []

        return "{} {} {}".format(self._intf, self._state, ", ".join(addr))

    def next(self):
        self._index += 1
        if self._index < len(self._interfaces):
            return True
        self._index = 0
        # reload to support hotplug
        self._interfaces = [ i for i in netifaces.interfaces() if not i.startswith(self._exclude) ]
        return False

    def _iswlan(self, intf):
        if not "wlan{}".format(intf) in self._cache:
            iw = pyroute2.IW()
            ip = pyroute2.IPRoute()
            idx = ip.link_lookup(ifname=intf)[0]
            try:
                iw.get_interface_by_ifindex(idx)
                self._cache["wlan{}".format(intf)] = True
            except Exception as e:
                self._cache["wlan{}".format(intf)] = False
        return self._cache["wlan{}".format(intf)]

    def _istunnel(self, intf):
        return intf.startswith("tun")

    def instance(self):
        return self._intf

    def state(self):
        t = "wireless" if self._iswlan(self._intf) else "wired"

        t = "tunnel" if self._istunnel(self._intf) else t

        return "{}-{}".format(t, self._state)

    def warning(self):
        return self._state != "up"

    def critical(self):
        return self._state == "down"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
