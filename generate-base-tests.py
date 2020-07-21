#!/usr/bin/env python

import os
import re
import sys
import glob


def is_psl(module):
    lib_path = os.path.dirname(os.__file__)
    old_sys = sys.path
    sys.path = [lib_path]
    is_psl = True
    try:
        __import__(module)
    except Exception as e:
        is_psl = False
    sys.path = old_sys

    return is_psl


def is_internal(module):
    if module.startswith("core.") or module == "core":
        return True
    if module.startswith("util.") or module == "util":
        return True
    if module.startswith("bumblebee_status."):
        return True
    if module.startswith("."):
        return True

    return is_psl(module)


def dependencies(filename):
    deps = []
    with open(filename) as f:
        for line in f:
            if "import" in line:
                match = re.match("\s*(from (\S+) )?import (\S+)", line)
                if not match:
                    continue
                dep = match.group(2) or match.group(3)
                if "util.popup" in dep or ("util" in line and "popup" in line):
                    deps.append("tkinter")
                if ".datetimetz" in line:
                    deps.extend(
                        dependencies("bumblebee_status/modules/contrib/datetimetz.py")
                    )
                elif not is_internal(dep):
                    deps.append(dep)
    return deps


def write_test(testname, modname, deps):
    fqmn = ".".join(["modules", testname.split(os.sep)[2], modname])
    if not os.path.exists(testname):
        with open(testname, "w") as f:
            f.writelines(
                ["import pytest\n\n",]
            )
            for dep in deps:
                f.write('pytest.importorskip("{}")\n\n'.format(dep))

    with open(testname) as f:
        for line in f:
            if "def test_load_module(" in line:
                print("skipping {}, already contains test".format(modname))
                return

    print("writing base test for {}".format(modname))
    with open(testname, "a+") as f:
        f.writelines(
            ["def test_load_module():\n", '    __import__("{}")\n\n'.format(fqmn),]
        )


def main():
    for f in glob.glob("bumblebee_status/modules/*/*.py"):
        if os.path.basename(f) == "__init__.py":
            continue

        modname = os.path.splitext(os.path.basename(f))[0]

        modpath = os.path.dirname(f)
        deps = dependencies(f)
        testname = os.path.join(
            "tests", "modules", modpath.split(os.sep)[2], "test_{}.py".format(modname)
        )

        write_test(testname, modname, deps)


if __name__ == "__main__":
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
