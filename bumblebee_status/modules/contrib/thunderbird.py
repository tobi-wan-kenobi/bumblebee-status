# pylint: disable=C0111,R0903

"""
Displays the unread emails count for one or more Thunderbird inboxes

Parameters:
    * thunderbird.home: Absolute path of your .thunderbird directory (e.g.: /home/pi/.thunderbird)
    * thunderbird.inboxes: Comma separated values for all MSF inboxes and their parent directory (account) (e.g.: imap.gmail.com/INBOX.msf,outlook.office365.com/Work.msf)

Tips:
    * You can run the following command in order to list all your Thunderbird inboxes

        find ~/.thunderbird -name '*.msf' | awk -F '/' '{print $(NF-1)"/"$(NF)}'

contributed by `cristianmiranda <https://github.com/cristianmiranda>`_ - many thanks!
"""

import core.module
import core.widget
import core.decorators
import core.input

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.thunderbird))

        self.__total = 0
        self.__label = ""
        self.__inboxes = []

        self.__home = self.parameter("home", "")
        inboxes = self.parameter("inboxes", "")
        if inboxes:
            self.__inboxes = util.format.aslist(inboxes)

    def thunderbird(self, _):
        return str(self.__label)

    def update(self):
        try:
            self.__total = 0
            self.__label = ""

            stream = self.__getThunderbirdStream()
            unread = self.__getUnreadMessagesByInbox(stream)

            counts = []
            for inbox in self.__inboxes:
                count = unread[inbox]
                self.__total += int(count)
                counts.append(count)

            self.__label = "/".join(counts)

        except Exception as err:
            self.__label = err

    def __getThunderbirdStream(self):
        cmd = (
            "find "
            + self.__home
            + " -name '*.msf' -exec grep -REo 'A2=[0-9]' {} + | grep"
        )
        for inbox in self.__inboxes:
            cmd += " -e {}".format(inbox)
        cmd += "| awk -F / '{print $(NF-1)\"/\"$(NF)}'"

        return util.cli.execute(cmd, shell=True).strip().split("\n")

    def __getUnreadMessagesByInbox(self, stream):
        unread = {}
        for line in stream:
            entry = line.split(":A2=")
            inbox = entry[0]
            count = entry[1]
            unread[inbox] = count

        return unread

    def state(self, widget):
        if self.__total > 0:
            return ["warning"]


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
