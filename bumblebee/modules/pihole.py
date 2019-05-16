# pylint: disable=C0111,R0903

"""Displays the pi-hole status (up/down) together with the number of ads that were blocked today
Parameters:
    * pihole.address     : pi-hole address (e.q: http://192.168.1.3)
    * pihole.pwhash      : pi-hole webinterface password hash (can be obtained from the /etc/pihole/SetupVars.conf file)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import requests

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.pihole_status)
        )

        buttons = {"LEFT_CLICK":bumblebee.input.LEFT_MOUSE}
        self._pihole_address = self.parameter("address", "")

        self._pihole_pw_hash = self.parameter("pwhash", "")
        self._pihole_status = None
        self._ads_blocked_today = "-"
        self.update_pihole_status()

        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
                                       cmd=self.toggle_pihole_status)

    def pihole_status(self, widget):
        if self._pihole_status is None:
            return "pi-hole unknown"
        return "pi-hole " + ("up/" + self._ads_blocked_today if self._pihole_status else "down")

    def update_pihole_status(self):
        try:
            data = requests.get(self._pihole_address + "/admin/api.php?summary").json()
            self._pihole_status = True if data["status"] == "enabled" else False
            self._ads_blocked_today = data["ads_blocked_today"]
        except:
            self._pihole_status = None

    def toggle_pihole_status(self, widget):
        if self._pihole_status is not None:
            try:
                req = None
                if self._pihole_status:
                    req = requests.get(self._pihole_address + "/admin/api.php?disable&auth=" + self._pihole_pw_hash)
                else:
                    req = requests.get(self._pihole_address + "/admin/api.php?enable&auth=" + self._pihole_pw_hash)
                if req is not None:
                    if req.status_code == 200:
                        status = req.json()["status"]
                        self._pihole_status = False if status == "disabled" else True
            except:
                pass


    def update(self, widgets):
        self.update_pihole_status()

    def state(self, widget):
        if self._pihole_status is None:
            return []
        elif self._pihole_status:
            return ["enabled"]
        return ["disabled", "warning"]
