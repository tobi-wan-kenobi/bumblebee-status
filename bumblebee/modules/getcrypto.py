# pylint: disable=C0111,R0903

"""Displays the price of a cryptocurrency.

Requires the following python packages:
    * requests

Parameters:
    * getcrypto.interval: Interval in seconds for updating the price, default is 120, less than that will probably get your IP banned.
    * getcrypto.getbtc: 0 for not getting price of BTC, 1 for getting it (default).
    * getcrypto.geteth: 0 for not getting price of ETH, 1 for getting it (default).
    * getcrypto.getltc: 0 for not getting price of LTC, 1 for getting it (default).
"""

import requests
import time
import bumblebee.input
import bumblebee.output
import bumblebee.engine

def getfromkrak(coin):
    if coin=='Btc':
        epair = "xbtusd"
        tickname = "XXBTZUSD"
    if coin=='Eth':
        epair = "ethusd"
        tickname = "XETHZUSD"
    if coin=='Ltc':
        epair = "ltcusd"
        tickname = "XLTCZUSD"
    krakenget = requests.get('https://api.kraken.com/0/public/Ticker?pair='+epair).json()
    kethusdask = float(krakenget['result'][tickname]['a'][0])
    kethusdbid = float(krakenget['result'][tickname]['b'][0])
    return coin+": "+str((kethusdask+kethusdbid)/2)[0:6]


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.curprice)
        )
        self._curprice = 0
        self._nextcheck = 0
        self._interval = int(self.parameter("interval", "120"))
        self._getbtc = int(self.parameter("getbtc", "1"))
        self._geteth = int(self.parameter("geteth", "1"))
        self._getltc = int(self.parameter("getltc", "1"))
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE,
            cmd="xdg-open https://cryptowat.ch/")

    def curprice(self, widget):
        return self._curprice

    def update(self, widgets):
        if self._nextcheck < int(time.time()):
            self._nextcheck = int(time.time()) + self._interval
            btcprice, ethprice, ltcprice = "", "", ""
            if self._getbtc==1:
                btcprice= getfromkrak('Btc')
            if self._geteth==1:
                ethprice=getfromkrak('Eth')
            if self._getltc==1:
                ltcprice=getfromkrak('Ltc')
            self._curprice = btcprice+" "*(self._getbtc*self._geteth)+ethprice+" "*(self._getltc*max(self._getbtc, self._geteth))+ltcprice

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
