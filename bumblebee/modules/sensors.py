# pylint: disable=C0111,R0903

"""Displays sensor temperature

Requires the following executable:
    * sensors

Parameters:
    * sensors.match: Line to match against output of 'sensors -u' (default: temp1_input)
    * sensors.match_number: which of the matches you want (default -1: last match).
"""

import re
import decimal

from subprocess import call

import bumblebee.input
import bumblebee.output
import bumblebee.engine

class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        super(Module, self).__init__(engine, config,
                                     bumblebee.output.Widget(full_text=self.temperature))
        self._temperature = "unknown"
        pattern = self.parameter("match", "temp1_input")
        pattern_string = r"^\s*{}:\s*([\d.]+)$".format(pattern)
        self._match_number = int(self.parameter("match_number", "-1"))
        self._pattern = re.compile(pattern_string, re.MULTILINE)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd="xsensors")

    def get_temp(self):
        temperatures = bumblebee.util.execute("sensors -u")
        matching_temp = self._pattern.findall(temperatures)
        temperature = "unknown"
        if matching_temp:
            temperature = int(float(matching_temp[self._match_number]))

        return temperature

    def get_mhz( self ):
        output = open( '/proc/cpuinfo' ).read()
        m      = re.search( r"cpu MHz\s+:\s+(\d+)", output )
        mhz    = int( m.group( 1 ) )

        if mhz < 1000:
            return "{} MHz".format( mhz )
        else:
            return "%.1f GHz" % ( decimal.Decimal( mhz ) / 1000 )

    def temperature(self, _):
        return u"{}°c @ {}".format( self._temperature, self._mhz )

    def update(self, widgets):
        self._temperature = self.get_temp()
        self._mhz = self.get_mhz()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
