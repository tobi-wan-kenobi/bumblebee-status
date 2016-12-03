import argparse

MODULE_HELP = ""

class Config(object):
    def __init__(self, args = []):
        parser = self._create_parser()
        self._args = parser.parse_args(args)

    def modules(self):
        return list(map(lambda x: { "name": x, "module": x }, self._args.modules))

    def _create_parser(self):
        parser = argparse.ArgumentParser(description="display system data in the i3bar")
        parser.add_argument("-m", "--modules", nargs="+", default = [],
            help = MODULE_HELP)
        return parser

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
