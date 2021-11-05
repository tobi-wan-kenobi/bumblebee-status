import os
import ast

from configparser import RawConfigParser

import sys
import glob
import textwrap
import argparse
import logging

import core.theme

import util.store
import util.format

import modules.core
import modules.contrib

log = logging.getLogger(__name__)

MODULE_HELP = "Specify a space-separated list of modules to load. The order of the list determines their order in the i3bar (from left to right). Use <module>:<alias> to provide an alias in case you want to load the same module multiple times, but specify different parameters."
PARAMETER_HELP = (
    "Provide configuration parameters in the form of <module>.<key>=<value>"
)
THEME_HELP = "Specify the theme to use for drawing modules"


def all_modules():
    """Returns a list of all available modules (either core or contrib)

    :return: list of modules
    :rtype: list of strings
    """
    result = {}

    for path in [modules.core.__file__, modules.contrib.__file__]:
        path = os.path.dirname(path)
        for mod in glob.iglob("{}/*.py".format(path)):
            result[os.path.basename(mod).replace(".py", "")] = 1

    res = list(result.keys())
    res.sort()
    return res


class print_usage(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        argparse.Action.__init__(self, option_strings, dest, nargs, **kwargs)
        self._indent = " " * 2

    def __call__(self, parser, namespace, value, option_string=None):
        if value == "modules":
            self._args = namespace
            self._format = "plain"
            self.print_modules()
        elif value == "modules-rst":
            self._args = namespace
            self._format = "rst"
            self.print_modules()
        elif value == "themes":
            self.print_themes()
        sys.exit(0)

    def print_themes(self):
        print(", ".join(core.theme.themes()))

    def print_modules(self):
        basepath = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
        )

        rst = {}

        if self._format == "rst":
            print(".. THIS DOCUMENT IS AUTO-GENERATED, DO NOT MODIFY")
            print(".. To change this document, please update the docstrings in the individual modules")

        for m in all_modules():
            try:
                module_type = "core"
                filename = os.path.join(basepath, "modules", "core", "{}.py".format(m))
                if not os.path.exists(filename):
                    filename = os.path.join(
                        basepath, "modules", "contrib", "{}.py".format(m)
                    )
                    module_type = "contrib"
                if not os.path.exists(filename):
                    log.warning("module {} not found".format(m))
                    continue

                doc = None
                with open(filename) as f:
                    tree = ast.parse(f.read())
                    doc = ast.get_docstring(tree)

                if not doc:
                    log.warning("failed to find docstring for {}".format(m))
                    continue
                if self._format == "rst":
                    if os.path.exists(
                        os.path.join(basepath, "..", "screenshots", "{}.png".format(m))
                    ):
                        doc = "{}\n\n.. image:: ../screenshots/{}.png".format(doc, m)

                    rst[module_type] = rst.get(module_type, [])
                    rst[module_type].append({"module": m, "content": doc})
                else:
                    print(
                        textwrap.fill(
                            "{}:".format(m),
                            80,
                            initial_indent=self._indent * 2,
                            subsequent_indent=self._indent * 2,
                        )
                    )
                    for line in doc.split("\n"):
                        print(
                            textwrap.fill(
                                line,
                                80,
                                initial_indent=self._indent * 3,
                                subsequent_indent=self._indent * 6,
                            )
                        )
            except Exception as e:
                log.warning(e)

        if self._format == "rst":
            print("List of modules\n===============")
            for k in ["core", "contrib"]:
                print("\n{}\n{}\n".format(k, "-" * len(k)))
                for mod in rst[k]:
                    print("\n{}\n{}\n".format(mod["module"], "~" * len(mod["module"])))
                    print(mod["content"])


class Config(util.store.Store):
    """Represents the configuration of bumblebee-status (either via config file or via CLI)

    :param args: The arguments passed via the commandline
    """

    def __init__(self, args):
        super(Config, self).__init__()

        parser = argparse.ArgumentParser(
            description="bumblebee-status is a modular, theme-able status line generator for the i3 window manager. https://github.com/tobi-wan-kenobi/bumblebee-status/wiki"
        )
        parser.add_argument(
            "-c",
            "--config-file",
            action="store",
            default=None,
            help="Specify a configuration file to use"
        )
        parser.add_argument(
            "-m", "--modules", nargs="+", action="append", default=[], help=MODULE_HELP
        )
        parser.add_argument(
            "-p",
            "--parameters",
            nargs="+",
            action="append",
            default=[],
            help=PARAMETER_HELP,
        )
        parser.add_argument("-t", "--theme", default=None, help=THEME_HELP)
        parser.add_argument(
            "-i",
            "--iconset",
            default="auto",
            help="Specify the name of an iconset to use (overrides theme default)",
        )
        parser.add_argument(
            "-a",
            "--autohide",
            nargs="+",
            default=[],
            help="Specify a list of modules to hide when not in warning/error state",
        )
        parser.add_argument(
            "-e",
            "--errorhide",
            nargs="+",
            default=[],
            help="Specify a list of modules that are hidden when in state error"
        )
        parser.add_argument(
            "-d", "--debug", action="store_true", help="Add debug fields to i3 output"
        )
        parser.add_argument(
            "-f",
            "--logfile",
            help="destination for the debug log file, if -d|--debug is specified; defaults to stderr",
        )
        parser.add_argument(
            "-r",
            "--right-to-left",
            action="store_true",
            help="Draw widgets from right to left, rather than left to right (which is the default)",
        )
        parser.add_argument(
            "-l",
            "--list",
            choices=["modules", "themes", "modules-rst"],
            help="Display a list of available themes or available modules, along with their parameters",
            action=print_usage,
        )

        self.__args = parser.parse_args(args)

        if self.__args.config_file:
            cfg = self.__args.config_file
            cfg = os.path.expanduser(cfg)
            self.load_config(cfg)
        else:
            for cfg in [
                "~/.bumblebee-status.conf",
                "~/.config/bumblebee-status.conf",
                "~/.config/bumblebee-status/config",
            ]:
                cfg = os.path.expanduser(cfg)
                self.load_config(cfg)

        parameters = [item for sub in self.__args.parameters for item in sub]
        for param in parameters:
            if not "=" in param:
                log.error(
                    'missing value for parameter "{}" - ignoring this parameter'.format(
                        param
                    )
                )
                continue
            key, value = param.split("=", 1)
            self.set(key, value)

    """Loads parameters from an init-style configuration file

    :param filename: path to the file to load
    """

    def load_config(self, filename):
        if os.path.exists(filename):
            log.info("loading {}".format(filename))
            tmp = RawConfigParser()
            tmp.read(u"{}".format(filename))

            if tmp.has_section("module-parameters"):
                for key, value in tmp.items("module-parameters"):
                    self.set(key, value)
            if tmp.has_section("core"):
                for key, value in tmp.items("core"):
                    self.set(key, value)


    """Returns a list of configured modules

    :return: list of configured (active) modules
    :rtype: list of strings
    """

    def modules(self):
        list_of_modules = [item for sub in self.__args.modules for item in sub]

        if list_of_modules == []:
            list_of_modules = util.format.aslist(self.get('modules', []))
        return list_of_modules

    """Returns the global update interval

    :return: update interval in seconds
    :rtype: float
    """

    def interval(self, default=1):
        return util.format.seconds(self.get("interval", default))

    """Returns whether debug mode is enabled

    :return: True if debug is enabled, False otherwise
    :rtype: boolean
    """

    def debug(self):
        return self.__args.debug

    """Returns whether module order should be reversed/inverted

    :return: True if modules should be reversed, False otherwise
    :rtype: boolean
    """

    def reverse(self):
        return self.__args.right_to_left

    """Returns the logfile location

    :return: location where the logfile should be written
    :rtype: string
    """

    def logfile(self):
        return self.__args.logfile

    """Returns the configured theme name

    :return: name of the configured theme
    :rtype: string
    """

    def theme(self):
        return self.__args.theme or self.get("theme") or "default"

    """Returns the configured iconset name

    :return: name of the configured iconset
    :rtype: string
    """

    def iconset(self):
        return self.__args.iconset

    """Returns whether a module should be hidden if their state is not warning/critical

    :return: True if module should be hidden automatically, False otherwise
    :rtype: bool
    """

    def autohide(self, name):
        return name in self.__args.autohide or name in util.format.aslist(self.get("autohide", []))

    """Returns which modules should be hidden if they are in state error

    :return: returns True if name should be hidden, False otherwise
    :rtype: bool
    """
    def errorhide(self, name):
        return name in self.__args.errorhide

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
