# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Displays currency exchange rates. Currently, displays currency between GBP and USD/EUR only.

Requires the following python packages:
    * requests

Parameters:
    * currency.interval: Interval in minutes between updates, default is 1.
    * currency.source: Source currency (ex. "GBP", "EUR"). Defaults to "auto", which infers the local one from IP address.
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
import json
import os

SYMBOL = {
    "GBP": u"£", "EUR": u"€", "USD": u"$", "JPY": u"¥", "KRW": u"₩"
}
DEFAULT_DEST = "USD,EUR,GBP"
DEFAULT_SRC = "auto"
DEFAULT_SRC_FALLBACK = "GBP"

API_URL = "https://markets.ft.com/data/currencies/ajax/conversion?baseCurrency={}&comparison={}"
LOCATION_URL = "https://ipvigilante.com/"


def get_local_country():
    r = requests.get(LOCATION_URL)
    location = r.json()
    return location['data']['country_name']


def load_country_to_currency():
    fname = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data', 'country-by-currency-code.json')
    with open(fname, 'r') as f:
        data = json.load(f)
    country2curr = {}
    for dt in data:
        country2curr[dt['country']] = dt['currency_code']

    return country2curr


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

        self._symbols = []
        for d in self.parameter("destination", DEFAULT_DEST).split(","):
            if d == 'auto':
                new = self.find_local_currency()
            else:
                new = d
            if new != self._base:
                self._symbols.append(new)

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
            country = get_local_country()
            currency_map = load_country_to_currency()
            return currency_map.get(country, DEFAULT_SRC_FALLBACK)
        except:
            return DEFAULT_SRC_FALLBACK

    def fmt_rate(self, rate):
        float_rate = float(rate.replace(',', ''))
        if not 0.01 < float_rate < 100:
            return rate
        else:
            return "%.3g" % float_rate

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
