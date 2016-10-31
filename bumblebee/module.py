
class Module(object):
    def __init__(self, theme, args):
        self._theme = theme

    def theme(self):
        return self._theme

    def data(self):
        pass

    def state(self):
        return "default"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
