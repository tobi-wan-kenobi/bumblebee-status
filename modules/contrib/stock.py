# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Display a stock quote from worldtradingdata.com

Requires the following python packages:
    * requests

Parameters:
    * stock.symbols : Comma-separated list of symbols to fetch
    * stock.change : Should we fetch change in stock value (defaults to True)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import bumblebee.util

import json
import requests

import logging

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.value)
        )
        self._symbols = self.parameter('symbols', '')
        self._change = bumblebee.util.asbool(self.parameter('change', True))
        self._value = None
        self.interval_factor(60)
        self.interval(60)

    def value(self, widget):
        results = []
        if not self._value:
            return 'n/a'
        data = json.loads(self._value)

        for symbol in data['quoteResponse']['result']:
            valkey = 'regularMarketChange' if self._change else 'regularMarketPrice'
            sym = 'n/a' if not 'symbol' in symbol else symbol['symbol']
            currency = 'USD' if not 'currency' in symbol else symbol['currency']
            val = 'n/a' if not valkey in symbol else '{:.2f}'.format(symbol[valkey])
            results.append('{} {} {}'.format(sym, val, currency))
        return u' '.join(results)

    def fetch(self):
        if self._symbols:
            url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols='
            url += self._symbols + '&fields=regularMarketPrice,currency,regularMarketChange'
            return requests.get(url).text.strip()
        else:
            logging.error('unable to retrieve stock exchange rate')
            return None

    def update(self, widgets):
        self._value = self.fetch()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
