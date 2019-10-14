# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Display a stock quote from worldtradingdata.com

Requires the following python packages:
    * requests

Parameters:
    * stock.symbols : Comma-separated list of symbols to fetch
    * stock.change : Should we fetch change in stock value (defaults to True)
    * stock.token : Your API token registered at https://worldtradingdata.com
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
        self._token = self.parameter('token', None)
        self._value = None
        self.interval(60)

    def value(self, widget):
        results = []
        if not self._value:
            return 'n/a'
        data = json.loads(self._value)

        for symbol in data['data']:
            val = 'day_change' if self._change else 'price'
            results.append('{} {}{}'.format(symbol['symbol'], symbol[val], symbol['currency']))
        return u' '.join(results)

    def fetch(self):
        if not self._token:
            logging.error('please specify a token')
            return None
        if self._symbols:
            url = 'https://api.worldtradingdata.com/api/v1/stock?'
            url += 'api_token={}'.format(self._token)
            url += '&symbol={}'.format(self._symbols)
            return requests.get(url).text.strip()
        else:
            logging.error('unable to retrieve stock exchange rate')
            return None

    def update(self, widgets):
        self._value = self.fetch()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
