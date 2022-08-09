"""Rofication indicator

    https://github.com/DaveDavenport/Rofication
    simple module to show an icon + the number of notifications stored in rofication
    module will have normal highlighting if there are zero notifications,
                     "warning" highlighting if there are nonzero notifications,
                     "critical" highlighting if there are any critical notifications

    Parameters:
    * rofication.regolith: Switch to regolith fork of rofication, see <https://github.com/regolith-linux/regolith-rofication>.

"""

import core.module
import core.widget
import core.decorators

import sys
import socket

class Module(core.module.Module):
    @core.decorators.every(seconds=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.__critical = False
        self.__numnotifications = 0
        self.__regolith = self.parameter("regolith", False)


    def full_text(self, widgets):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect("/tmp/rofi_notification_daemon")
            # below code will fetch two numbers in a list, e.g. ['22', '1']
            # first is total number of notifications, second is number of critical notifications
            if self.__regolith:
                client.sendall(bytes("num\n", "utf-8"))
            else:
                client.sendall(bytes("num", "utf-8"))
            val = client.recv(512)
            val = val.decode("utf-8")
            if self.__regolith:
                l = val.split(',',2)
            else:
                l = val.split('\n',2)
            self.__numnotifications = int(l[0])
            self.__critical = bool(int(l[1]))
            return self.__numnotifications

    def state(self, widget):
        # rofication doesn't really support the idea of seen vs unseen notifications
        # marking a message as "seen" actually just sets its urgency to normal
        # so, doing highlighting if any notifications are present
        if self.__critical:
            return ["critical"]
        elif self.__numnotifications:
            return ["warning"]
        return []

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
