"""
Show progress for cp, mv, dd, ...

Parameters:
   * progress.placeholder: Text to display while no process is running (defaults to "n/a")
   * progress.barwidth: Width of the progressbar if it is used (defaults to 8)
   * progress.format: Format string (defaults to "{bar} {cmd} {arg}")
                      Available values are: {bar} {pid} {cmd} {arg} {per} {qty}

Requires the following executable:
   * progress
"""

import bumblebee.input
import bumblebee.output
import bumblebee.engine

import re


class Module(bumblebee.engine.Module):

    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
            bumblebee.output.Widget(full_text=self.get_progress_text)
        )

    def get_progress_text(self, widget):
        if self.update_progress_info(widget):
            width = self.parameter("barwidth", 8)
            count = round((width * widget.get("per")) / 100)
            bar = "[{}{}]".format(
                "#" * count,
                "--" * (width - count)
            )

            str_format = self.parameter("format", '{bar} {cmd} {arg}')
            return "  " + str_format.format(
                bar = bar,
                pid = widget.get("pid"),
                cmd = widget.get("cmd"),
                arg = widget.get("arg"),
                per = widget.get("per"),
                qty = widget.get("qty")
            )
        else:
            return self.parameter("placeholder", 'n/a')

    def update_progress_info(self, widget):
        # This regex extracts following groups:
        #  1. pid
        #  2. command
        #  3. arguments
        #  4. progress (xx.x formated)
        #  5. quantity (.. unit / .. unit formated)
        extract_nospeed = re.compile("\[ *(\d*)\] ([a-zA-Z]*) (.*)\n\t(\d*\.*\d*)% \((.*)\)\n.*")

        try:
            raw = bumblebee.util.execute("progress -q")
            result = extract_nospeed.match(raw)

            widget.set("pid", int(result.group(1)))
            widget.set("cmd", result.group(2))
            widget.set("arg", result.group(3))
            widget.set("per", float(result.group(4)))
            widget.set("qty", result.group(5))
            return True
        except Exception:
            return False

