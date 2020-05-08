# pylint: disable=C0111,R0903

"""Displays the pi-hole status (up/down) together with the number of ads that were blocked today

Parameters:
    * pihole.address     : pi-hole address (e.q: http://192.168.1.3)
    * pihole.pwhash      : pi-hole webinterface password hash (can be obtained from the /etc/pihole/SetupVars.conf file)

contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""

import requests

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.pihole_status))

        self._pihole_address = self.parameter("address", "")
        self._pihole_pw_hash = self.parameter("pwhash", "")
        self._pihole_status = None
        self._ads_blocked_today = "-"
        self.update_pihole_status()

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.toggle_pihole_status
        )

    def pihole_status(self, widget):
        if self._pihole_status is None:
            return "pi-hole unknown"
        return "pi-hole {}".format(
            "up {} blocked".format(self._ads_blocked_today)
            if self._pihole_status
            else "down"
        )

    def update_pihole_status(self):
        try:
            data = requests.get(self._pihole_address + "/admin/api.php?summary").json()
            self._pihole_status = True if data["status"] == "enabled" else False
            self._ads_blocked_today = data["ads_blocked_today"]
        except Exception as e:
            self._pihole_status = None

    def toggle_pihole_status(self, widget):
        if self._pihole_status is not None:
            try:
                req = None
                if self._pihole_status:
                    req = requests.get(
                        self._pihole_address
                        + "/admin/api.php?disable&auth="
                        + self._pihole_pw_hash
                    )
                else:
                    req = requests.get(
                        self._pihole_address
                        + "/admin/api.php?enable&auth="
                        + self._pihole_pw_hash
                    )
                if req is not None:
                    if req.status_code == 200:
                        status = req.json()["status"]
                        self._pihole_status = False if status == "disabled" else True
            except:
                pass

    def update(self):
        self.update_pihole_status()

    def state(self, widget):
        if self._pihole_status is None:
            return []
        elif self._pihole_status:
            return ["enabled"]
        return ["disabled", "warning"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
