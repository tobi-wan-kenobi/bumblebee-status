# -*- coding: utf-8 -*-

"""Displays the number of docker containers running

Requires the following python packages:
    * docker

contributed by `jlopezzarza <https://github.com/jlopezzarza>`_ - many thanks!
"""

import docker

from requests.exceptions import ConnectionError

import core.module
import core.widget
import core.decorators


class Module(core.module.Module):
    @core.decorators.every(seconds=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.docker_info))
        self.__info = ""

    def state(self, widget):
        state = []
        if self.__info == "OK - 0":
            state.append("warning")
        elif self.__info in ["n/a", "off"]:
            state.append("critical")
        return state

    def docker_info(self, widget):
        try:
            cli = docker.DockerClient(base_url="unix://var/run/docker.sock")
            cli.ping()
            self.__info = "OK - {}".format(
                len(cli.containers.list(filters={"status": "running"}))
            )
        except ConnectionError:
            self.__info = "off"
        except Exception:
            self.__info = "n/a"
        return self.__info


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
