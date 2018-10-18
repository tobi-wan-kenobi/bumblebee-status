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
        widget = bumblebee.output.Widget(full_text=self.status)
        super(Module, self).__init__(engine, config, widget)
        self._status = self.status

    def update(self, widgets):
        self._status = self.status

    def status(self, _):
        cli = docker.DockerClient(base_url='unix://var/run/docker.sock')
        try:
            cli.ping()
        except ConnectionError:
            return "Daemon off"
        return "OK - {}".format(len(cli.containers.list(filters={'status': "running"})))
