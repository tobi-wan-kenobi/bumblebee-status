# pylint: disable=C0111,R0903

"""Displays the Octorrint status and the printer's bed/tools temperature in the status bar.

   Left click opens a popup which shows the bed & tools temperatures and additionally a livestream of the webcam (if enabled).

Prerequisites:
    * tk python library (usually python-tk or python3-tk, depending on your distribution)

Parameters:
    * octoprint.address     : Octoprint address (e.q: http://192.168.1.3)
    * octoprint.apitoken    : Octorpint API Token (can be obtained from the Octoprint Webinterface)
    * octoprint.webcam      : Set to True if a webcam is connected (default: False)

contributed by `bbernhard <https://github.com/bbernhard>`_ - many thanks!
"""


import urllib
import logging
import threading
import queue

import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk

import requests
import simplejson

import core.module
import core.widget
import core.input


def get_frame(url):
    img_bytes = b""
    stream = urllib.request.urlopen(url)
    while True:
        img_bytes += stream.read(1024)
        a = img_bytes.find(b"\xff\xd8")
        b = img_bytes.find(b"\xff\xd9")
        if a != -1 and b != -1:
            jpg = img_bytes[a : b + 2]
            img_bytes = img_bytes[b + 2 :]
            img = Image.open(BytesIO(jpg))
            return img
    return None


class WebcamImagesWorker(threading.Thread):
    def __init__(self, url, queue):
        threading.Thread.__init__(self)

        self.__url = url
        self.__queue = queue
        self.__running = True

    def run(self):
        while self.__running:
            img = get_frame(self.__url)
            self.__queue.put(img)

    def stop(self):
        self.__running = False


class Module(core.module.Module):
    @core.decorators.every(seconds=5)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.octoprint_status))

        self.__octoprint_state = "Unknown"
        self.__octoprint_address = self.parameter("address", "")
        self.__octoprint_api_token = self.parameter("apitoken", "")
        self.__octoprint_webcam = self.parameter("webcam", False)

        self.__webcam_images_worker = None
        self.__webcam_image_url = self.__octoprint_address + "/webcam/?action=stream"
        self.__webcam_images_queue = None

        self.__printer_bed_temperature = "-"
        self.__tool1_temperature = "-"

        core.input.register(self, button=core.input.LEFT_MOUSE, cmd=self.__show_popup)

    def octoprint_status(self, widget):
        if (
            self.__octoprint_state.startswith("Offline")
            or self.__octoprint_state == "Unknown"
        ):
            return (
                (self.__octoprint_state[:25] + "...")
                if len(self.__octoprint_state) > 25
                else self.__octoprint_state
            )
        return (
            self.__octoprint_state
            + " | B: "
            + str(self.__printer_bed_temperature)
            + "°C"
            + " | T1: "
            + str(self.__tool1_temperature)
            + "°C"
        )

    def __get(self, endpoint):
        url = self.__octoprint_address + "/api/" + endpoint
        headers = {"X-Api-Key": self.__octoprint_api_token}
        resp = requests.get(url, headers=headers)

        try:
            return resp.json(), resp.status_code
        except simplejson.errors.JSONDecodeError:
            return None, resp.status_code

    def __get_printer_bed_temperature(self):
        printer_info, status_code = self.__get("printer")
        if status_code == 200:
            return (
                printer_info["temperature"]["bed"]["actual"],
                printer_info["temperature"]["bed"]["target"],
            )
        return None, None

    def __get_octoprint_state(self):
        job_info, status_code = self.__get("job")
        return job_info["state"] if status_code == 200 else "Unknown"

    def __get_tool_temperatures(self):
        tool_temperatures = []

        printer_info, status_code = self.__get("printer")
        if status_code == 200:
            temperatures = printer_info["temperature"]

            tool_id = 0
            while True:
                try:
                    tool = temperatures["tool" + str(tool_id)]
                    tool_temperatures.append((tool["actual"], tool["target"]))
                except KeyError:
                    break
                tool_id += 1
        return tool_temperatures

    def update(self):
        try:
            self.__octoprint_state = self.__get_octoprint_state()

            actual_temp, _ = self.__get_printer_bed_temperature()
            if actual_temp is None:
                actual_temp = "-"
            self.__printer_bed_temperature = str(actual_temp)

            tool_temps = self.__get_tool_temperatures()
            if len(tool_temps) > 0:
                self.__tool1_temperature = tool_temps[0][0]
            else:
                self.__tool1_temperature = "-"
        except Exception as e:
            logging.exception("Couldn't get data")

    def __refresh_image(self, root, webcam_image, webcam_image_container):
        try:
            img = self.__webcam_images_queue.get()
            webcam_image = ImageTk.PhotoImage(img)
            webcam_image_container.config(image=webcam_image)
        except queue.Empty as e:
            pass
        except Exception as e:
            logging.exception("Couldn't refresh image")

        root.after(5, self.__refresh_image, root, webcam_image, webcam_image_container)

    def __refresh_temperatures(
        self, root, printer_bed_temperature_label, tools_temperature_label
    ):
        actual_bed_temp, target_bed_temp = self.__get_printer_bed_temperature()
        if actual_bed_temp is None:
            actual_bed_temp = "-"
        if target_bed_temp is None:
            target_bed_temp = "-"

        bed_temp = "Bed: " + str(actual_bed_temp) + "/" + str(target_bed_temp) + " °C"
        printer_bed_temperature_label.config(text=bed_temp)

        tool_temperatures = self.__get_tool_temperatures()
        tools_temp = "Tools: "

        if len(tool_temperatures) == 0:
            tools_temp += "-/- °C"
        else:
            for i, tool_temperature in enumerate(tool_temperatures):
                tools_temp += (
                    str(tool_temperature[0]) + "/" + str(tool_temperature[1]) + "°C"
                )
                if i != len(tool_temperatures) - 1:
                    tools_temp += "\t"
        tools_temperature_label.config(text=tools_temp)

        root.after(
            500,
            self.__refresh_temperatures,
            root,
            printer_bed_temperature_label,
            tools_temperature_label,
        )

    def __show_popup(self, widget):
        root = tk.Tk()
        root.attributes("-type", "dialog")
        root.title("Octoprint")
        frame = tk.Frame(root)
        if self.__octoprint_webcam:

            # load first image synchronous before popup is shown, otherwise tkinter isn't able to layout popup properly
            img = get_frame(self.__webcam_image_url)
            webcam_image = ImageTk.PhotoImage(img)
            webcam_image_container = tk.Button(frame, image=webcam_image)
            webcam_image_container.pack()

            self.__webcam_images_queue = queue.Queue()

            self.__webcam_images_worker = WebcamImagesWorker(
                self.__webcam_image_url, self.__webcam_images_queue
            )
            self.__webcam_images_worker.start()
        else:
            logging.debug(
                "Not using webcam, as webcam is disabled. Enable with --webcam."
            )
        frame.pack()

        temperatures_label = tk.Label(frame, text="Temperatures", font=("", 25))
        temperatures_label.pack()

        printer_bed_temperature_label = tk.Label(
            frame, text="Bed: -/- °C", font=("", 15)
        )
        printer_bed_temperature_label.pack()

        tools_temperature_label = tk.Label(frame, text="Tools: -/- °C", font=("", 15))
        tools_temperature_label.pack()

        root.after(10, self.__refresh_image, root, webcam_image, webcam_image_container)
        root.after(
            500,
            self.__refresh_temperatures,
            root,
            printer_bed_temperature_label,
            tools_temperature_label,
        )
        root.bind("<Destroy>", self.__on_close_popup)

        root.eval("tk::PlaceWindow . center")
        root.mainloop()

    def __on_close_popup(self, event):
        self.__webcam_images_queue = None
        self.__webcam_images_worker.stop()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
