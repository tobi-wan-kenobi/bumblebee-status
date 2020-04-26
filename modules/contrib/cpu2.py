"""Multiwidget CPU module

Can display any combination of:

    * max CPU frequency
    * total CPU load in percents (integer value)
    * per-core CPU load as graph - either mono or colored
    * CPU temperature (in Celsius degrees)
    * CPU fan speed

Requirements:

    * the psutil Python module for the first three items from the list above
    * sensors executable for the rest

Parameters:
    * cpu2.layout: Space-separated list of widgets to add.
      Possible widgets are:
        * cpu2.maxfreq
        * cpu2.cpuload
        * cpu2.coresload
        * cpu2.temp
        * cpu2.fanspeed
    * cpu2.colored: 1 for colored per core load graph, 0 for mono (default)
                    if this is set to 1, use --markup=pango
    * cpu2.temp_pattern: pattern to look for in the output of 'sensors -u';
                         required if cpu2.temp widged is used
    * cpu2.fan_pattern: pattern to look for in the output of 'sensors -u';
                        required if cpu2.fanspeed widged is used

Note: if you are getting "n/a" for CPU temperature / fan speed, then you're
lacking the aforementioned pattern settings or they have wrong values.

"""

try:
    import psutil
except ImportError:
    pass

import bumblebee.engine
import bumblebee.util
import bumblebee.output


class Module(bumblebee.engine.Module):

    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config, [])
        self._layout = self.parameter("layout", "cpu2.maxfreq cpu2.cpuload cpu2.coresload cpu2.temp cpu2.fanspeed")
        self._widget_names = self._layout.split()
        widget_list = []
        for widget_name in self._widget_names:
            if widget_name == "cpu2.maxfreq":
                widget = bumblebee.output.Widget(
                    name=widget_name, full_text=self.maxfreq)
                widget.set("type", "freq")
            elif widget_name == "cpu2.cpuload":
                widget = bumblebee.output.Widget(
                    name=widget_name, full_text=self.cpuload)
                widget.set("type", "load")
            elif widget_name == "cpu2.coresload":
                widget = bumblebee.output.Widget(
                    name=widget_name, full_text=self.coresload)
                widget.set("type", "loads")
            elif widget_name == "cpu2.temp":
                widget = bumblebee.output.Widget(
                    name=widget_name, full_text=self.temp)
                widget.set("type", "temp")
            elif widget_name == "cpu2.fanspeed":
                widget = bumblebee.output.Widget(
                    name=widget_name, full_text=self.fanspeed)
                widget.set("type", "fan")
            widget_list.append(widget)
        self.widgets(widget_list)
        self._colored = bumblebee.util.asbool(self.parameter("colored", 0))
        self._temp_pattern = self.parameter("temp_pattern")
        if self._temp_pattern is None:
            self._temp = "n/a"
        self._fan_pattern = self.parameter("fan_pattern")
        if self._fan_pattern is None:
            self._fan = "n/a"
        # maxfreq is loaded only once at startup
        if "cpu2.maxfreq" in self._widget_names:
            self._maxfreq = psutil.cpu_freq().max / 1000
        self.update(widget_list)

    def maxfreq(self, _):
        return "{:.2f}GHz".format(self._maxfreq)

    def cpuload(self, _):
        return "{:>3}%".format(self._cpuload)

    def add_color(self, bar):
        """add color as pango markup to a bar"""
        if bar in ["▁", "▂"]:
            color = self.theme().color("green", "green")
        elif bar in ["▃", "▄"]:
            color = self.theme().color("yellow", "yellow")
        elif bar in ["▅", "▆"]:
            color = self.theme().color("orange", "orange")
        elif bar in ["▇", "█"]:
            color = self.theme().color("red", "red")
        colored_bar = "<span foreground='{}'>{}</span>".format(color, bar)
        return colored_bar

    def coresload(self, _):
        mono_bars = [bumblebee.output.hbar(x) for x in self._coresload]
        if not self._colored:
            return "".join(mono_bars)
        colored_bars = [self.add_color(x) for x in mono_bars]
        return "".join(colored_bars)

    def temp(self, _):
        if self._temp == "n/a" or self._temp == 0:
            return "n/a"
        return "{}°C".format(self._temp)

    def fanspeed(self, _):
        if self._fanspeed == "n/a":
            return "n/a"
        return "{}RPM".format(self._fanspeed)

    def _parse_sensors_output(self):
        output = bumblebee.util.execute("sensors -u")
        lines = output.split("\n")
        temp = "n/a"
        fan = "n/a"
        temp_line = None
        fan_line = None
        for line in lines:
            if self._temp_pattern is not None and self._temp_pattern in line:
                temp_line = line
            if self._fan_pattern is not None and self._fan_pattern in line:
                fan_line = line
            if temp_line is not None and fan_line is not None:
                break
        if temp_line is not None:
            temp = round(float(temp_line.split(":")[1].strip()))
        if fan_line is not None:
            fan = int(fan_line.split(":")[1].strip()[:-4])
        return temp, fan

    def update(self, _):
        if "cpu2.maxfreq" in self._widget_names:
            self._maxfreq = psutil.cpu_freq().max / 1000
        if "cpu2.cpuload" in self._widget_names:
            self._cpuload = round(psutil.cpu_percent(percpu=False))
        if "cpu2.coresload" in self._widget_names:
            self._coresload = psutil.cpu_percent(percpu=True)
        if "cpu2.temp" in self._widget_names or "cpu2.fanspeed" in self._widget_names:
            self._temp, self._fanspeed = self._parse_sensors_output()

    def state(self, widget):
        """for having per-widget icons"""
        return [widget.get("type", "")]
