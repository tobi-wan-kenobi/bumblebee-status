"""Retrieves location information from an external
service and caches it for 12h (retries are done every
30m in case of problems)

Right now, it uses (in order of preference):
    - http://free.ipwhois.io/
    - http://ipapi.co/
"""


import json
import time
import urllib.request

__document = None
__data = {}
__next = 0
__sources = [
    {
        "url": "http://ipapi.co/json",
        "mapping": {
            "latitude": "latitude",
            "longitude": "longitude",
            "country_name": "country",
            "ip": "public_ip",
        },
    },
    {
        "url": "http://free.ipwhois.io/json/",
        "mapping": {
            "latitude": "latitude",
            "longitude": "longitude",
            "country": "country",
            "ip": "public_ip",
        },
    }
]


def __expired():
    global __next
    return __next <= time.time()


def __load():
    global __data
    global __next

    __data = {}
    for src in __sources:
        try:
            tmp = json.loads(urllib.request.urlopen(src["url"]).read())
            for k, v in src["mapping"].items():
                __data[v] = tmp.get(k, None)
            __next = time.time() + 60 * 60 * 12  # update once every 12h
            return
        except Exception as e:
            pass
    __next = time.time() + 60 * 30  # error - try again every 30m


def __get(name, default=None):
    global __data
    if not __data or __expired():
        __load()
    return __data.get(name, default)


def reset():
    """Resets the location library, ensuring that a new query will be started
    """
    global __next
    __next = 0


def coordinates():
    """Returns a latitude, longitude pair

    :return: current latitude and longitude
    :rtype: pair of strings
    """
    return __get("latitude"), __get("longitude")


def country():
    """Returns the current country name

    :return: country name
    :rtype: string
    """
    return __get("country")


def public_ip():
    """Returns the current public IP

    :return: public IP
    :rtype: string
    """
    return __get("public_ip")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
