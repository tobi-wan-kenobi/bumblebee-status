# -*- coding: utf-8 -*-

"""Fetch hard drive temeperature data from a hddtemp daemon
that runs on localhost and default port (7634)
"""

import socket

import bumblebee.engine
import bumblebee.output

HOST = "localhost"
PORT = 7634

CHUNK_SIZE = 1024
RECORD_SIZE = 5
SEPARATOR = "|"


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.hddtemps)
        super(Module, self).__init__(engine, config, widget)
        self._hddtemps = self._get_hddtemps()

    def hddtemps(self, __):
        return self._hddtemps

    def _fetch_data(self):
        """fetch data from hddtemp service"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((HOST, PORT))
                data = ""
                while True:
                    chunk = sock.recv(CHUNK_SIZE)
                    if chunk:
                        data += str(chunk)
                    else:
                        break
            return data
        except (AttributeError, socket.error) as e:
            pass

    @staticmethod
    def _get_parts(data):
        """
            split data using | separator and remove first item
            (because the first item is empty)
        """
        parts = data.split("|")[1:]
        return parts

    @staticmethod
    def _partition_parts(parts):
        """
            partition parts: one device record is five (5) items
        """
        per_disk = [parts[i:i+RECORD_SIZE]
                    for i in range(len(parts))[::RECORD_SIZE]]
        return per_disk

    @staticmethod
    def _get_name_and_temp(device_record):
        """
            get device name (without /dev part, to save space on bar)
            and temperature (in °C) as tuple
        """
        device_name = device_record[0].split("/")[-1]
        device_temp = device_record[2]
        return (device_name, device_temp)

    @staticmethod
    def _get_hddtemp(device_record):
        name, temp = device_record
        hddtemp = "{}+{}°C".format(name, temp)
        return hddtemp

    def _get_hddtemps(self):
        data = self._fetch_data()
        if data is None:
            return "n/a"
        parts = self._get_parts(data)
        per_disk = self._partition_parts(parts)
        names_and_temps = [self._get_name_and_temp(x) for x in per_disk]
        hddtemps = [self._get_hddtemp(x) for x in names_and_temps]
        return SEPARATOR.join(hddtemps)

    def update(self, __):
        self._hddtemps = self._get_hddtemps()
