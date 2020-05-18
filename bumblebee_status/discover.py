import os
import sys


def discover():
    libdir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "bumblebee_status")
    )
    sys.path.append(libdir)


def utility(name):
    current_path = os.path.dirname(os.path.abspath(__file__))

    for path in [
        os.path.join(current_path, "..", "bin"),
        os.path.join(
            current_path, "..", "..", "..", "..", "share", "bumblebee-status", "utility"
        ),
        "/usr/share/bumblebee-status/bin/",
    ]:
        if os.path.exists(os.path.abspath(os.path.join(path, name))):
            return os.path.abspath(os.path.join(path, name))
    raise Exception("{} not found".format(name))


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
