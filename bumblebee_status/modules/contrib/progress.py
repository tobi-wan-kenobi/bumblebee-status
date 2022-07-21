"""
Show progress for cp, mv, dd, ...

Parameters:
   * progress.placeholder: Text to display while no process is running (defaults to 'n/a')
   * progress.barwidth: Width of the progressbar if it is used (defaults to 8)
   * progress.format: Format string (defaults to '{bar} {cmd} {arg}')
     Available values are: {bar} {pid} {cmd} {arg} {percentage} {quantity} {speed} {time}
   * progress.barfilledchar: Character used to draw the filled part of the bar (defaults to '#'), notice that it can be a string
   * progress.baremptychar: Character used to draw the empty part of the bar (defaults to '-'), notice that it can be a string

Requires the following executable:
   * progress

contributed by `remi-dupre <https://github.com/remi-dupre>`_ - many thanks!
"""

import core.module
import core.widget

import util.cli
import util.format

import re


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.get_progress_text))
        self.__active = False

    def hidden(self):
        return not self.__active

    def get_progress_text(self, widget):
        if self.update_progress_info(widget):
            width = util.format.asint(self.parameter("barwidth", 8))
            count = round((width * widget.get("per")) / 100)
            filledchar = self.parameter("barfilledchar", "#")
            emptychar = self.parameter("baremptychar", "-")

            bar = "[{}{}]".format(filledchar * count, emptychar * (width - count))

            str_format = self.parameter("format", "{bar} {cmd} {arg}")
            return str_format.format(
                bar=bar,
                pid=widget.get("pid"),
                cmd=widget.get("cmd"),
                arg=widget.get("arg"),
                percentage=widget.get("per"),
                quantity=widget.get("qty"),
                speed=widget.get("spd"),
                time=widget.get("tim"),
            )
        else:
            return self.parameter("placeholder", "n/a")

    def update_progress_info(self, widget):
        """Update widget's information about the copy"""
        if not self.__active:
            return

        # These regex extracts following groups:
        #  1. pid
        #  2. command
        #  3. arguments
        #  4. progress (xx.x formatted)
        #  5. quantity (.. unit / .. unit formatted)
        #  6. speed
        #  7. time remaining
        extract_nospeed = re.compile(
            r"\[ *(\d*)\] ([a-zA-Z]*) (.*)\n\t(\d*\.*\d*)% \((.*)\)\n.*"
        )
        extract_wtspeed = re.compile(
            r"\[ *(\d*)\] ([a-zA-Z]*) (.*)\n\t(\d*\.*\d*)% \((.*)\) (\d*\.\d .*) remaining (\d*:\d*:\d*)\n.*"
        )

        try:
            raw = util.cli.execute("progress -qW 0.1")
            result = extract_wtspeed.match(raw)

            if not result:
                # Abort speed measures
                raw = util.cli.execute("progress -q")
                result = extract_nospeed.match(raw)

                widget.set("spd", "???.? B/s")
                widget.set("tim", "??:??:??")
            else:
                widget.set("spd", result.group(6))
                widget.set("tim", result.group(7))

            widget.set("pid", int(result.group(1)))
            widget.set("cmd", result.group(2))
            widget.set("arg", result.group(3))
            widget.set("per", float(result.group(4)))
            widget.set("qty", result.group(5))
            return True
        except Exception:
            return False

    def update(self):
        self.__active = bool(util.cli.execute("progress -q"))

    def state(self, widget):
        if self.__active:
            return ["copying", "no-autohide"]
        return "pending"


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
