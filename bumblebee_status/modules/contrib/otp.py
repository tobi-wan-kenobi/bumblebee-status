"""One Time Pin Generator

* Requires:
    * pyotpi
    * keyring
    * xclip for click to copy to clipboard
    
* Parameters(both required):
    * opt.service_name: service name where secret_key is stored in keyring
    * opt.user_name: username for keyring where secret_key is store

contributed by `theymightbetim <https://github.com/theymightbetim>`
"""

import core.module
import core.widget
import core.input

import pyotp
import keyring


class Module(core.module.Module):

    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__username = self.parameter("user_name", "not set")
        self.__service_name = self.parameter("service_name", "not set")
        self.__key = keyring.get_password(self.__service_name, self.__username)
        self.__totp = pyotp.TOTP(self.__key)
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.copy_to_clipboard
        )

    def full_text(self, widget):
        if self.__service_name == "not set":
            return "ConfigError: otp.service_name not set"
        if self.__username == "not set":
            return "ConfigError: otp.user_name not set"
        return self.__totp.now()

    def copy_to_clipboard(self, event):
        import subprocess

        mfa_code = str(self.__totp.now())
        subprocess.Popen(["xclip", "-i"], stdin=subprocess.PIPE).communicate(
            mfa_code.encode("utf-8")
        )
