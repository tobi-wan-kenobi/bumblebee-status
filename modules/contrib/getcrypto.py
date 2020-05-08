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

contributed by `Ryunaq <https://github.com/Ryunaq>`_ - many thanks!
"""

import requests
from requests.exceptions import RequestException
import time

import core.module
import core.widget
import core.input
import core.decorators

import util.format


def getfromkrak(coin, currency):
    abbrev = {
        "Btc": ["xbt", "XXBTZ"],
        "Eth": ["eth", "XETHZ"],
        "Ltc": ["ltc", "XLTCZ"],
    }
    data = abbrev.get(coin, None)
    if not data:
        return
    epair = "{}{}".format(data[0], currency)
    tickname = "{}{}".format(data[1], currency.upper())
    try:
        krakenget = requests.get(
            "https://api.kraken.com/0/public/Ticker?pair=" + epair
        ).json()
    except (RequestException, Exception):
        return "No connection"
    if not "result" in krakenget:
        return "No data"
    kethusdask = float(krakenget["result"][tickname]["a"][0])
    kethusdbid = float(krakenget["result"][tickname]["b"][0])
    return coin + ": " + str((kethusdask + kethusdbid) / 2)[0:6]


class Module(core.module.Module):
    @core.decorators.every(minutes=30)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.curprice))

        self.__curprice = ""
        self.__getbtc = util.format.asbool(self.parameter("getbtc", True))
        self.__geteth = util.format.asbool(self.parameter("geteth", True))
        self.__getltc = util.format.asbool(self.parameter("getltc", True))
        self.__getcur = self.parameter("getcur", "usd")
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd="xdg-open https://cryptowat.ch/"
        )

    def curprice(self, widget):
        return self.__curprice

    def update(self):
        currency = self.__getcur
        btcprice, ethprice, ltcprice = "", "", ""
        if self.__getbtc:
            btcprice = getfromkrak("Btc", currency)
        if self.__geteth:
            ethprice = getfromkrak("Eth", currency)
        if self.__getltc:
            ltcprice = getfromkrak("Ltc", currency)
        self.__curprice = (
            btcprice
            + " " * (self.__getbtc * self.__geteth)
            + ethprice
            + " " * (self.__getltc * max(self.__getbtc, self.__geteth))
            + ltcprice
        )


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
