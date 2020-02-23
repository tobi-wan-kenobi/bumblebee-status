from .__pulseaudio import Module

class Module(Module):
    def __init__(self, config):
        super().__init__(config, 'source')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
