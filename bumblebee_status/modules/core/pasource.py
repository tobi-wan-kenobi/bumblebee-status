from .pulseaudio import Module


class Module(Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, "source")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
