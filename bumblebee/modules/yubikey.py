# pylint: disable=C0111,R0903

"""Shows yubikey information

Requires: https://github.com/Yubico/python-yubico

The output indicates that a YubiKey is not connected or it displays
the corresponding serial number.

"""

import yubico

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.keystate))
        self._keystate = "No YubiKey"

    def keystate(self, widget):
        return self._keystate

    def update(self, widget):
        try:
            self._keystate = "YubiKey: " + str(yubico.find_yubikey(debug=False).serial())
        except yubico.yubico_exception.YubicoError:
            self._keystate = "No YubiKey"

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
