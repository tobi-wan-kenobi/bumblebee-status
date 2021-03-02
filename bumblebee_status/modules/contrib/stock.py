# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Display a stock quote from finance.yahoo.com

Parameters:
    * stock.symbols : Comma-separated list of symbols to fetch
    * stock.change : Should we fetch change in stock value (defaults to True)


contributed by `msoulier <https://github.com/msoulier>`_ - many thanks!
"""

import json
import urllib.request

import logging

import core.module
import core.widget
import core.decorators

import util.format


class Module(core.module.Module):
    @core.decorators.every(hours=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.value))

        self.__symbols = self.parameter("symbols", "")
        self.__change = util.format.asbool(self.parameter("change", True))
        self.__value = None

    def value(self, widget):
        results = []
        if not self.__value:
            return "n/a"
        data = json.loads(self.__value)

        for symbol in data["quoteResponse"]["result"]:
            valkey = "regularMarketChange" if self.__change else "regularMarketPrice"
            sym = symbol.get("symbol", "n/a")
            currency = symbol.get("currency", "USD")
            val = "n/a" if not valkey in symbol else "{:.2f}".format(symbol[valkey])
            results.append("{} {} {}".format(sym, val, currency))
        return " ".join(results)

    def fetch(self):
        if self.__symbols:
            url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
            url += (
                self.__symbols
                + "&fields=regularMarketPrice,currency,regularMarketChange"
            )
            try:
                return urllib.request.urlopen(url).read().strip()
            except urllib.request.URLError:
                logging.error("unable to open stock exchange url")
                return None
        else:
            logging.error("unable to retrieve stock exchange rate")
            return None

    def update(self):
        self.__value = self.fetch()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
