import os
import sys


def discover():
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bumblebee_status"))
    sys.path.append(libdir)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
