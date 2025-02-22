# pylint: disable=C0111,R0903

"""Displays the pi-hole status (up/down) together with the number of ads that were blocked today

Parameters:
    * pihole.address     : pi-hole address (e.q: http://192.168.1.3)


    * pihole.apitoken    : pi-hole API token (can be obtained in the pi-hole webinterface (Settings -> API)


contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""

from enum import Enum
from datetime import date
from datetime import datetime
import logging
import requests
import core.module
import core.widget
import core.input


# Pi-hole API documentation:
# https://ftl.pi-hole.net/development/docs/


class PiholeApiError(Enum):
    NOERROR = 1
    AUTHENTICATIONERROR = 2
    GENERALERROR = 3


class Module(core.module.Module):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.pihole_status))

        self._pihole_address = self.parameter("address", "")
        self._pihole_api_token = self.parameter("apitoken", "")

        self._pihole_error = PiholeApiError.NOERROR
        self._pihole_enabled = False
        self._session_id = None
        self._ads_blocked_today = "-"
        self._update_pihole_status()

        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self._toggle_pihole_status
        )

    def _authenticate(self):
        try:
            payload = {"password": self._pihole_api_token}
            resp = requests.post(self._pihole_address + "/api/auth", json=payload)
            if resp.status_code == 200:
                self._session_id = resp.json()["session"]["sid"]
            elif resp.status_code == 401:
                self._pihole_error = PiholeApiError.AUTHENTICATIONERROR
        except Exception as e:
            logging.error(str(e))
            self._pihole_error = PiholeApiError.AUTHENTICATIONERROR

    def pihole_status(self, widget):
        if self._pihole_error == PiholeApiError.GENERALERROR:
            return "pi-hole unknown"
        if self._pihole_error == PiholeApiError.AUTHENTICATIONERROR:
            return "pi-hole auth error"
        return "pi-hole {}".format(
            "up {} blocked".format(self._ads_blocked_today)
            if self._pihole_enabled
            else "down"
        )

    def _fetch_blocking_status(self):
        try:
            resp = requests.get(
                self._pihole_address + "/api/dns/blocking",
                headers={"sid": self._session_id},
            )
            if resp.status_code == 200:
                self._pihole_enabled = (
                    True if resp.json()["blocking"] == "enabled" else False
                )
            elif resp.status_code == 401:
                self._pihole_error = PiholeApiError.AUTHENTICATIONERROR
        except Exception as e:
            logging.error(str(e))
            self._pihole_error = PiholeApiError.GENERALERROR

    def _fetch_blocked_ads_statistics(self):
        try:
            current_date = date.today()
            from_timestamp = datetime(
                current_date.year, current_date.month, current_date.day, 0, 0, 0
            ).timestamp()
            to_timestamp = datetime(
                current_date.year, current_date.month, current_date.day, 23, 59, 59
            ).timestamp()
            params = {
                "upstream": "blocklist",
                "from": from_timestamp,
                "until": to_timestamp,
            }
            resp = requests.get(
                self._pihole_address + "/api/queries",
                params=params,
                headers={"sid": self._session_id},
            )
            if resp.status_code == 200:
                self._ads_blocked_today = resp.json()["recordsFiltered"]
        except Exception as e:
            logging.error(str(e))
            self._pihole_error = PiholeApiError.GENERALERROR

    def _update_pihole_status(self):
        if self._session_id is None:
            self._authenticate()

        if self._session_id is not None:
            self._fetch_blocking_status()
            self._fetch_blocked_ads_statistics()

    def _toggle_pihole_status(self, widget):
        if self._pihole_error == PiholeApiError.NOERROR:
            try:
                payload = {}
                payload["blocking"] = False if self._pihole_enabled else True
                resp = requests.post(
                    self._pihole_address + "/api/dns/blocking",
                    json=payload,
                    headers={"sid": self._session_id},
                )
                if resp.status_code == 200:
                    self._pihole_enabled = not self._pihole_enabled
                elif resp.status_code == 401:
                    self._pihole_error = PiholeApiError.AUTHENTICATIONERROR
            except Exception as e:
                logging.error(str(e))

    def update(self):
        self._update_pihole_status()

    def state(self, widget):
        if self._pihole_error != PiholeApiError.NOERROR:
            return []
        if self._pihole_enabled:
            return ["enabled"]
        return ["disabled", "warning"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
