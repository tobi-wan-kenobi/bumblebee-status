# -*- coding: utf-8 -*-

"""Displays the number of docker containers running

Requires the following python packages:
    * docker

"""

try:
    import docker
except ImportError:
    pass

from requests.exceptions import ConnectionError

import bumblebee.input
import bumblebee.output
import bumblebee.engine


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widgets = bumblebee.output.Widget(full_text=self.status)
        super(Module, self).__init__(engine, config, widgets)
        self._status = self.status
        self._state = self.state

    def update(self, widgets):
        self._status = self.status
        self._state = self.state

    def state(self, widget):
        state = []
        status = self.status(widget)
        if status == "OK - 0":
            state.append("warning")
        elif  status in ["n/a", "Daemon off"]:
            state.append("critical")
        return state

    def status(self, widget):
        try:
            cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
            cli.ping()
        except ConnectionError:
            return "Daemon off"
        except Exception:
            return "n/a"
        return "OK - {}".format(len(cli.containers.list(filters={'status': "running"})))
