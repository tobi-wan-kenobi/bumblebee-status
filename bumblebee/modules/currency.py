# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays currency exchange rates. Currently, displays currency between GBP and USD/EUR only.

Requires the following python packages:
    * requests

Parameters:
    * currency.interval: Interval in minutes between updates, default is 1.
    * currency.source: Source currency (defaults to "GBP")
    * currency.destination: Comma-separated list of destination currencies (defaults to "USD,EUR")
    * currency.sourceformat: String format for source formatting; Defaults to "{}: {}" and has two variables,
                             the base symbol and the rate list
    * currency.destinationdelimiter: Delimiter used for separating individual rates (defaults to "|")

Note: source and destination names right now must correspond to the names used by the API of https://markets.ft.com
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
try:
    import requests
except ImportError:
    pass

SYMBOL = {
    "GBP": u"£", "EUR": u"€", "USD": u"$", "JPY": u"¥"
}

API_URL = "https://markets.ft.com/data/currencies/ajax/conversion?baseCurrency={}&comparison={}"

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.price)
        )
        self._data = []
        self.interval(1)
        self._base = self.parameter("source", "GBP")
        self._symbols = self.parameter("destination", "USD,EUR").split(",")
        self._nextcheck = 0

    def price(self, widget):
        if len(self._data) == 0:
            return "?"

        rates = []
        for sym, rate in self._data:
            rates.append(u"{}{}".format(rate, SYMBOL[sym] if sym in SYMBOL else sym))

        basefmt = u"{}".format(self.parameter("sourceformat", "{}: {}"))
        ratefmt = u"{}".format(self.parameter("destinationdelimiter", "|"))

        return basefmt.format(SYMBOL[self._base] if self._base in SYMBOL else self._base, ratefmt.join(rates))

    def update(self, widgets):
        self._data = []
        for symbol in self._symbols:
            url = API_URL.format(self._base, symbol)
            try:
                response = requests.get(url).json()
                self._data.append((symbol, response['data']['exchangeRate']))
            except Exception:
                pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
