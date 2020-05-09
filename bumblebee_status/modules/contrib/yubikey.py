# pylint: disable=C0111,R0903

"""Shows yubikey information

Requires: https://github.com/Yubico/python-yubico

The output indicates that a YubiKey is not connected or it displays
the corresponding serial number.


contributed by `EmmaTinten <https://github.com/EmmaTinten>`_ - many thanks!
"""

import yubico

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(seconds=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.keystate))
        self.__keystate = "No YubiKey"

    def keystate(self, widget):
        return self.__keystate

    def update(self):
        try:
            self.__keystate = "YubiKey: " + str(
                yubico.find_yubikey(debug=False).serial()
            )
        except yubico.yubico_exception.YubicoError:
            self.__keystate = "No YubiKey"
        except Exception:
            self.__keystate = "n/a"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
