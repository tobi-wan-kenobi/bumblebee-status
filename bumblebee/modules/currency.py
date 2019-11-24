# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays currency exchange rates. Currently, displays currency between GBP and USD/EUR only.

Requires the following python packages:
    * requests

Parameters:
    * currency.interval: Interval in minutes between updates, default is 1.
    * currency.source: Source currency (defaults to "GBP"). Set to "auto" infer the local one.
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
    "GBP": u"£", "EUR": u"€", "USD": u"$", "JPY": u"¥", "KRW": u"₩"
}
DEFAULT_DEST = "USD,EUR,GBP"
DEFAULT_SRC = "auto"

API_URL = "https://markets.ft.com/data/currencies/ajax/conversion?baseCurrency={}&comparison={}"

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.price)
        )
        self._data = []
        self.interval_factor(60)
        self.interval(1)
        self._nextcheck = 0

        src = self.parameter("source", DEFAULT_SRC)
        if src == "auto":
            self._base = self.find_local_currency()
        else:
            self._base = src

        dest = [d for d in self.parameter("destination", DEFAULT_DEST).split(",")
                if d != self._base]
        self._symbols = dest


    def price(self, widget):
        if len(self._data) == 0:
            return "?"

        rates = []
        for sym, rate in self._data:
            rate = self.fmt_rate(rate)
            rates.append(u"{}{}".format(rate, SYMBOL[sym] if sym in SYMBOL else sym))

        basefmt = u"{}".format(self.parameter("sourceformat", "1{}={}"))
        ratefmt = u"{}".format(self.parameter("destinationdelimiter", "="))

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

    def find_local_currency(self):
        '''Use geolocation lookup to find local currency'''
        try:
            r = requests.get('https://ipvigilante.com/')
            if not r.ok: return DEFAULT_SRC
            dt = r.json()
            if dt['status'] != 'success':
                return DEFAULT_SRC
            country = dt['data']['country_name']

            r = requests.get("https://raw.githubusercontent.com/samayo/country-json/master/src/country-by-currency-code.json")
            if not r.ok: return DEFAULT_SRC
            data = r.json()
            country2curr = {}
            for dt in data:
                country2curr[dt['country']] = dt['currency_code']

            return country2curr.get(country, DEFAULT_SRC)
        except:
            return DEFAULT_SRC

    def fmt_rate(self, rate):
        float_rate = float(rate.replace(',', ''))
        if not 0.01 < float_rate < 100:
            return rate
        else:
            return "%.3g" % float_rate

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
