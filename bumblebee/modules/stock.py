# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Display a stock quote from yahoo finance.

Requires the following python packages:
    * requests

Parameters:
    * stock.symbols : Comma-separated list of symbols to fetch
    * stock.change : Should we fetch change in stock value (defaults to True)
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine
import requests
from requests.exceptions import RequestException

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.value)
        )
        self._symbols = self.parameter("symbols", "")
        self._change = self.parameter("change", True)
        self._baseurl = 'http://download.finance.yahoo.com/d/quotes.csv'
        self._value = self.fetch()

    def value(self, widget):
        results = ["$%s" % val for val in self._value.split('\n')]
        return ' '.join(results)

    def fetch(self):
        if self._symbols:
            url = self._baseurl
            url += '?s=%s&f=l1' % self._symbols
            if self._change:
                url += 'c1'
            return requests.get(url).text.strip()
        else:
            return ''

    def update(self, widgets):
        self._value = self.fetch()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
