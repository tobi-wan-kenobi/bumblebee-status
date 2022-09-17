#!/bin/bash

import sys
import json
import hashlib
import requests

rv = requests.request(
    "GET",
    "https://api.github.com/repos/tobi-wan-kenobi/bumblebee-status/releases/latest",
)

if rv.status_code != 200:
    sys.exit(1)

release = json.loads(rv.text)

tar = requests.get(f"https://github.com/tobi-wan-kenobi/bumblebee-status/archive/{release['name']}.tar.gz")
checksum = hashlib.sha512(tar.content).hexdigest()

template = ""
with open("./PKGBUILD.template") as f:
    template = f.read()

template = template.replace("<PKGVERSION>", release["name"].lstrip("v"))
template = template.replace("<SHA512SUM>", checksum)

print(template)
