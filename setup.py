#!/usr/bin/env python
"""Setup file for bumbleestatus bar to allow pip install of full package"""
# -*- coding: utf8 - *-
from setuptools import setup, find_packages
import versioneer

with open("requirements/base.txt") as f:
    INSTALL_REQS = [line for line in f.read().split("\n") if line]

# Module packages
def read_module(filename):
    """Read each in a module's requirements and parse it for extras"""
    with open("requirements/modules/{}.txt".format(filename)) as fname:
        return [rline for rline in fname.read().split("\n") if rline]


EXTRAS_REQUIREMENTS_MAP = {
    "battery-upower": read_module("battery_upower_reqs"),
    "cpu": read_module("cpu"),
    "cpu2": read_module("cpu2"),
    "currency": read_module("currency"),
    "docker_ps": read_module("docker_ps"),
    "getcrypto": read_module("getcrypto"),
    "git": read_module("git"),
    "github": read_module("github"),
    "layout-xkb": read_module("layout_xkb"),
    "memory": read_module("memory"),
    "network_traffic": read_module("network_traffic"),
    "nic": read_module("nic"),
    "pihole": read_module("pihole"),
    "rss": read_module("rss"),
    "spaceapi": read_module("spaceapi"),
    "spotify": read_module("spotify"),
    "stock": read_module("stock"),
    "sun": read_module("sun"),
    "system": read_module("system"),
    "taskwarrior": read_module("taskwarrior"),
    "title": read_module("title"),
    "traffic": read_module("traffic"),
    "weather": read_module("weather"),
    "yubikey": read_module("yubikey"),
}

import glob

setup(
    #    packages=["bumblebee-status-packages"],
    #    package_dir={"bumblebee-status-packages": "."},
    install_requires=INSTALL_REQS,
    extras_require=EXTRAS_REQUIREMENTS_MAP,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
    test_suite="tests",
    data_files=[
        ("share/bumblebee-status/themes", glob.glob("themes/*.json")),
        ("share/bumblebee-status/themes/icons", glob.glob("themes/icons/*.json")),
        ("share/bumblebee-status/utility", glob.glob("bin/*")),
        ("share/man/man1", glob.glob("man/*.1")),
    ],
    packages=find_packages(exclude=["tests", "tests.*"])
)
