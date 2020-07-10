# pylint: disable=C0111,R0903

"""
Displays the message that's received via unix socket.

Parameteres:
    * messagereceiver   : Unix socket address (e.g: /tmp/bumblebee_messagereceiver.sock)
"""

import core.module
import core.widget
import core.input

import socket
import threading
import logging
import os
import queue
import json


class Worker(threading.Thread):
    def __init__(self, unix_socket_address, queue):
        threading.Thread.__init__(self)
        self.__unix_socket_address = unix_socket_address
        self.__queue = queue

    def run(self):
        while True:
            try:
                os.unlink(self.__unix_socket_address)
            except OSError as e:
                if os.path.exists(self.__unix_socket_address):
                    logging.exception(
                        "Couldn't bind to unix socket %s" % self.__unix_socket_address
                    )
                    raise

            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.bind(self.__unix_socket_address)
                s.listen()

                conn, _ = s.accept()
                with conn:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.__queue.put(data.decode("utf-8"))


class Module(core.module.Module):
    @core.decorators.every(seconds=1)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.message))

        self.__unix_socket_address = self.parameter("address", "")

        self.__message = ""
        self.__state = []

        self.__queue = queue.Queue()
        self.__worker = Worker(self.__unix_socket_address, self.__queue)
        self.__worker.daemon = True
        self.__worker.start()

    def message(self, widget):
        return self.__message

    def update(self):
        try:
            received_data = self.__queue.get(block=False)
            parsed_data = json.loads(received_data)
            self.__message = parsed_data["message"]
            self.__state = parsed_data["state"]
        except json.JSONDecodeError as e:
            logging.exception("Couldn't parse message")
        except queue.Empty as e:
            pass

    def state(self, widget):
        return self.__state


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
