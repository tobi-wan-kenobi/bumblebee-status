# pylint: disable=C0111,R0903

"""
Displays the message that's received via unix socket.

Parameters:
    * messagereceiver   : Unix socket address (e.g: /tmp/bumblebee_messagereceiver.sock)

Example:
    The following examples assume that /tmp/bumblebee_messagereceiver.sock is used as unix socket address.
    
    In order to send the string "I  bumblebee-status" to your status bar, use the following command: 
        echo -e '{"message":"I  bumblebee-status", "state": ""}' | socat unix-connect:/tmp/bumblebee_messagereceiver.sock STDIO

    In order to highlight the text, the state variable can be used: 
        echo -e '{"message":"I  bumblebee-status", "state": "warning"}' | socat unix-connect:/tmp/bumblebee_messagereceiver.sock STDIO

contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""

import socket
import logging
import os
import json

import core.module
import core.widget
import core.input


class Module(core.module.Module):
    @core.decorators.never
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.message))

        self.background = True

        self.__unix_socket_address = self.parameter("address", "")

        self.__message = ""
        self.__state = []

    def message(self, widget):
        return self.__message

    def __read_data_from_socket(self):
        while True:
            try:
                os.unlink(self.__unix_socket_address)
            except OSError:
                if os.path.exists(self.__unix_socket_address):
                    logging.exception(
                        "Couldn't bind to unix socket %s", self.__unix_socket_address
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
                        yield data.decode("utf-8")

    def update(self):
        try:
            for received_data in self.__read_data_from_socket():
                parsed_data = json.loads(received_data)
                self.__message = parsed_data["message"]
                self.__state = parsed_data["state"]
                core.event.trigger("update", [self.id], redraw_only=True)
        except json.JSONDecodeError:
            logging.exception("Couldn't parse message")
        except Exception:
            logging.exception("Unexpected exception while reading from socket")

    def state(self, widget):
        return self.__state


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
