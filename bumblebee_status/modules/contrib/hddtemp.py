# -*- coding: utf-8 -*-

"""Fetch hard drive temperature data from a hddtemp daemon
that runs on localhost and default port (7634)

contributed by `somospocos <https://github.com/somospocos>`_ - many thanks!
"""

import socket

import core.module
import core.widget

HOST = "localhost"
PORT = 7634

CHUNK_SIZE = 1024
RECORD_SIZE = 5
SEPARATOR = "|"


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.hddtemps))
        self.__hddtemps = self.__get_hddtemps()

    def hddtemps(self, _):
        return self.__hddtemps

    def __fetch_data(self):
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
    def __get_parts(data):
        """
            split data using | separator and remove first item
            (because the first item is empty)
        """
        parts = data.split("|")[1:]
        return parts

    @staticmethod
    def __partition_parts(parts):
        """
            partition parts: one device record is five (5) items
        """
        per_disk = [
            parts[i : i + RECORD_SIZE] for i in range(len(parts))[::RECORD_SIZE]
        ]
        return per_disk

    @staticmethod
    def __get_name_and_temp(device_record):
        """
            get device name (without /dev part, to save space on bar)
            and temperature (in °C) as tuple
        """
        device_name = device_record[0].split("/")[-1]
        device_temp = device_record[2]
        return (device_name, device_temp)

    @staticmethod
    def __get_hddtemp(device_record):
        name, temp = device_record
        hddtemp = "{}+{}°C".format(name, temp)
        return hddtemp

    def __get_hddtemps(self):
        data = self.__fetch_data()
        if data is None:
            return "n/a"
        parts = self.__get_parts(data)
        per_disk = self.__partition_parts(parts)
        names_and_temps = [self.__get_name_and_temp(x) for x in per_disk]
        hddtemps = [self.__get_hddtemp(x) for x in names_and_temps]
        return SEPARATOR.join(hddtemps)

    def update(self):
        self.__hddtemps = self.__get_hddtemps()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
