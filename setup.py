#!/usr/bin/env python
# -*- coding: utf8 - *-
import sys

from setuptools import setup, Extension

about = {}
with open("bumblebee/__about__.py") as fp:
    exec(fp.read(), about)

with open('requirements/base.txt') as f:
    install_reqs = [line for line in f.read().split('\n') if line]

# Module packages
def read_module(filename):
    with open('requirements/modules/{}.txt'.format(filename)) as f:
        return [line for line in f.read().split('\n') if line]

EXTRAS_REQUIREMENTS_MAP = {
    "battery-upower": read_module("battery_upower_reqs"),
    "cpu": read_module("cpu"),
    "cpu2": read_module("cpu2"),
    "currency": read_module("currency"),
    "docker_ps": read_module("docker_ps"),
    "dunst": read_module("dunst"),
    "getcrypto": read_module("getcrypto"),
    "git": read_module("git"),
    "github": read_module("github"),
    "hddtemp": read_module("hddtemp"),
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

if sys.version_info[0] > 2:
    readme = open('README.md', encoding='utf-8').read()
else:
    readme = open('README.md').read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    url=about['__github__'],
    download_url=about['__pypi__'],
    project_urls={
        'Documentation': about['__docs__'],
        'Code': about['__github__'],
        'Issue tracker': about['__tracker__'],
    },
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['bumblebee'],
    include_package_data=True,
    install_requires=install_reqs,
    extras_require=EXTRAS_REQUIREMENTS_MAP,
    zip_safe=False,
    keywords=about['__title__'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Utilities",
    ],
)
