# -*- coding: UTF-8 -*-
# pylint: disable=C0111,R0903

"""Display a stock quote from finance.yahoo.com

Parameters:
    * stock.symbols : Comma-separated list of symbols to fetch
    * stock.apikey : API key created on https://alphavantage.co
    * stock.url : URL to use, defaults to "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}"
    * stock.fields : Fields from the response to show, defaults to "01. symbol,05. price,10. change percent"


contributed by `msoulier <https://github.com/msoulier>`_ - many thanks!
"""

import json
import urllib.request

import logging

import core.module
import core.widget
import core.decorators

import util.format

def flatten(d, result):
    for k, v in d.items():
        if type(v) is dict:
            flatten(v, result)
        else:
            result[k] = v

class Module(core.module.Module):
    @core.decorators.every(hours=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.value))

        self.__symbols = self.parameter("symbols", "")
        self.__apikey = self.parameter("apikey", None)
        self.__fields = self.parameter("fields", "01. symbol,05. price,10. change percent").split(",")
        self.__url = self.parameter("url", "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}")
        self.__change = util.format.asbool(self.parameter("change", True))
        self.__values = []


    def value(self, widget):
        result = ""

        for value in self.__values:
            res = {}
            flatten(value, res)
            for field in self.__fields:
                result += res.get(field, "n/a") + " "
        result = result[:-1]
        return result

    def fetch(self):
        results = []
        if self.__symbols:
            for symbol in self.__symbols.split(","):
                url = self.__url.format(symbol=symbol, apikey=self.__apikey)
                try:
                    results.append(json.loads(urllib.request.urlopen(url).read().strip()))
                except urllib.request.URLError:
                    logging.error("unable to open stock exchange url")
                    return []
        else:
            logging.error("unable to retrieve stock exchange rate")
            return []
        return results

    def update(self):
        self.__values = self.fetch()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
