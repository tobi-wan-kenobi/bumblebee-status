# pylint: disable=C0111,R0903

"""Displays the price of a cryptocurrency.

Requires the following python packages:
    * requests

Parameters:
    * getcrypto.interval: Interval in seconds for updating the price, default is 120, less than that will probably get your IP banned.
    * getcrypto.getbtc: 0 for not getting price of BTC, 1 for getting it (default).
    * getcrypto.geteth: 0 for not getting price of ETH, 1 for getting it (default).
    * getcrypto.getltc: 0 for not getting price of LTC, 1 for getting it (default).
    * getcrypto.getcur: Set the currency to display the price in, usd is the default.
"""

import requests
import time
import bumblebee.util
import bumblebee.input
import bumblebee.output
import bumblebee.engine
from requests.exceptions import RequestException
def getfromkrak(coin,currency):
    abbrev = {
        "Btc": ["xbt", "XXBTZ"],
        "Eth": ["eth", "XETHZ"],
        "Ltc": ["ltc", "XLTCZ"],
    }
    data = abbrev.get(coin, None)
    if not data: return
    epair = "{}{}".format(data[0], currency)
    tickname = "{}{}".format(data[1], currency.upper())
    try:
        krakenget = requests.get('https://api.kraken.com/0/public/Ticker?pair='+epair).json()
    except (RequestException, Exception):
        return "No connection"
    kethusdask = float(krakenget['result'][tickname]['a'][0])
    kethusdbid = float(krakenget['result'][tickname]['b'][0])
    return coin+": "+str((kethusdask+kethusdbid)/2)[0:6]


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.curprice)
        )
        self._curprice = ""
        self._nextcheck = 0
        self._interval = int(self.parameter("interval", "120"))
        self._getbtc = bumblebee.util.asbool(self.parameter("getbtc", True))
        self._geteth = bumblebee.util.asbool(self.parameter("geteth", True))
        self._getltc = bumblebee.util.asbool(self.parameter("getltc", True))
        self._getcur = self.parameter("getcur", "usd")
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="xdg-open https://cryptowat.ch/")

    def curprice(self, widget):
        return self._curprice

    def update(self, widgets):
        if self._nextcheck < int(time.time()):
            self._nextcheck = int(time.time()) + self._interval
            currency = self._getcur
            btcprice, ethprice, ltcprice = "", "", ""
            if self._getbtc:
                btcprice= getfromkrak('Btc',currency)
            if self._geteth:
                ethprice=getfromkrak('Eth',currency)
            if self._getltc:
                ltcprice=getfromkrak('Ltc',currency)
            self._curprice = btcprice+" "*(self._getbtc*self._geteth)+ethprice+" "*(self._getltc*max(self._getbtc, self._geteth))+ltcprice

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
