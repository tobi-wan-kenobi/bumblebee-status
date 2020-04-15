import json
import time
import urllib.request

__document = None
__data = {}
__next = 0

__sources = [
        {
            'url': 'http://free.ipwhois.io/json/',
            'mapping': {
                'latitude': 'latitude',
                'longitude': 'longitude',
                'country': 'country',
                'ip': 'public_ip',
            }
        },
        {
            'url': 'http://ipapi.co/json',
            'mapping': {
                'latitude': 'latitude',
                'longitude': 'longitude',
                'country_name': 'country',
                'ip': 'public_ip',
            }
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
            tmp = json.loads(urllib.request.urlopen(src['url']).read())
            for k, v in src['mapping'].items():
                __data[v] = tmp.get(k, None)
            __next = time.time() + 60*60*12 # update once every 12h
            return
        except Exception as e:
            pass
    __next = time.time() + 60*30 # error - try again every 30m

def __get(name, default=None):
    global __data
    if not __data or __expired():
        __load()
    return __data.get(name, default)

def reset():
    global __next
    __next = 0

def coordinates():
    return __get('latitude'), __get('longitude')

def country():
    return __get('country')

def public_ip():
    return __get('public_ip')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
