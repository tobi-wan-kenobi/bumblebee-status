"""Displays air quality data using the aerlive.ro service (Romania only)

Parameters:
    * aerlive.unit: Measurement unit: ica (default), ica_co, ica_no2, ica_pm1,
        ica_pm10, ica_pm25, ica_so2
    * aerlive.city: City ID (currently only Bucharest (BUC) and Cluj-Napoca
        (CJ) are supported)
"""

from collections import namedtuple
from requests import RequestException

import core.module
import core.widget
import core.input
import core.decorators
import requests

Measurement = namedtuple(
    "Measurement",
    ["location", "unit_value", "ica_value"],
)

ICA_WARNING_THRESHOLD = 49
ICA_CRITICAL_THRESHOLD = 74

AERLIVE_REQUEST_URL = "https://apps.roiot.ro/aerlive/api-v2/data.php"
AERLIVE_REQUEST_KEY = "d09668ea-def5-44ea-8c77-ae32e9fa5572"


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(
            config,
            theme,
            core.widget.Widget(self.text),  # type: ignore
        )

        self.unit = self.parameter("unit", "ica")
        self.city = self.parameter("city")

        self.measurements = []
        self.current_index = -1

        # Avoid unneeded POST requests
        self.is_fetch_data_needed = True

        # Cycle through the registered locations using the left click
        core.input.register(
            self,
            button=core.input.LEFT_MOUSE,
            cmd=self.next_location,
        )

        # Reset the location (to the one with the highest level of
        # pollution) using the right click
        core.input.register(
            self,
            button=core.input.RIGHT_MOUSE,
            cmd=self.reset_location,
        )

    def update(self):
        if not self.is_fetch_data_needed:
            return

        json_data_list = []

        try:
            json_data_list = requests.post(
                AERLIVE_REQUEST_URL,
                data={
                    "key": AERLIVE_REQUEST_KEY,
                    "city": self.city,
                },
                stream=True
            ).json()["data"][:-1]
        except RequestException:
            pass

        self.measurements = []

        for json_data in json_data_list:
            try:
                location = json_data["name"]
                unit_value = round(json_data["highest"][self.unit])
                ica_value = round(json_data["highest"]["ica"])
            except TypeError:
                continue

            measurement = Measurement(location, unit_value, ica_value)
            self.measurements.append(measurement)

        self.reset_measurement_index()

    def text(self, _):
        self.is_fetch_data_needed = True

        if not self.measurements:
            return "?"

        measurement = self.measurements[self.current_index]
        return f"{measurement.location} {measurement.unit_value}"

    def next_location(self, _):
        self.is_fetch_data_needed = False

        if not self.measurements:
            return

        self.current_index = (self.current_index + 1) % len(self.measurements)

    def state(self, _):  # type: ignore
        ica_value = 0

        if self.measurements:
            ica_value = self.measurements[self.current_index].ica_value

        # Thresholding is done based on the ICA value, just like on the
        # original website
        return [
            self.threshold_state(
                ica_value,
                ICA_WARNING_THRESHOLD,
                ICA_CRITICAL_THRESHOLD,
            )
        ]

    def reset_measurement_index(self):
        if not self.measurements:
            self.current_index = -1
            return

        # Select the measurement with the largest value
        unit_values = [x.unit_value for x in self.measurements]
        self.current_index = unit_values.index(max(unit_values))

    def reset_location(self, _):
        self.is_fetch_data_needed = False
        self.reset_measurement_index()
