"""Retrieves location information from an external
service and caches it for 12h (retries are done every
30m in case of problems)

Right now, it uses (in order of preference):
    - http://free.ipwhois.io/ - 10k free requests/month
    - http://ipapi.co/ - 30k free requests/month
    - http://ip-api.com/ - ~2m free requests/month

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
            "country_name": "country_name",
            "country_code": "country_code",
            "city": "city_name",
            "ip": "public_ip",
        },
    },
    {
        "url": "http://free.ipwhois.io/json/",
        "mapping": {
            "latitude": "latitude",
            "longitude": "longitude",
            "country": "country_name",
            "country_code": "country_code",
            "city": "city_name",
            "ip": "public_ip",
        },
    },
    {
        "url": "http://ip-api.com/json",
        "mapping": {
            "latitude": "lat",
            "longitude": "lon",
            "country": "country_name",
            "countryCode": "country_code",
            "city": "city_name",
            "query": "public_ip",
        },
    },
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


def __get(name):
    global __data
    if not __data or __expired():
        __load()
    if name in __data:
        return __data[name]
    else:
        return None


def reset():
    """Resets the location library, ensuring that a new query will be started"""
    global __next
    global __data

    __data = None
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
    return __get("country_name")


def country_code():
    """Returns the current country code

    :return: country code
    :rtype: string
    """
    return __get("country_code")


def city_name():
    """Returns the current city name

    :return: city name
    :rtype: string
    """
    return __get("city_name")


def public_ip():
    """Returns the current public IP

    :return: public IP
    :rtype: string
    """
    return __get("public_ip")


def location_info():
    """Returns the current location information

    :return: public IP, country name, country code, city name & coordinates
    :rtype: dictionary
    """
    return {
        "public_ip": __get("public_ip"),
        "country": __get("country_name"),
        "country_code": __get("country_code"),
        "city_name": __get("city_name"),
        "latitude": __get("latitude"),
        "longitude": __get("longitude"),
    }


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
