# pylint: disable=C0111,R0903,W1401

""" Execute command in shell and print result

Few command examples:
    'ping 1.1.1.1 -c 1 | grep -Po "(?<=time=)\d+(\.\d+)? ms"'
    'echo "BTC=$(curl -s rate.sx/1BTC | grep -Po \"^\d+\")USD"'
    'curl -s https://wttr.in/London?format=%l+%t+%h+%w'
    'pip3 freeze | wc -l'
    'any_custom_script.sh | grep arguments'

Parameters:
    * shell.command:  Command to execute
                      Use single parentheses if evaluating anything inside (sh-style)
                      For example shell.command='echo $(date +"%H:%M:%S")'
                      But NOT shell.command="echo $(date +'%H:%M:%S')"
                      Second one will be evaluated only once at startup
    * shell.interval: Update interval in seconds
                      (defaults to 1s == every bumblebee-status update)
    * shell.async:    Run update in async mode. Won't run next thread if
                      previous one didn't finished yet. Useful for long
                      running scripts to avoid bumblebee-status freezes
                      (defaults to False)
"""

import os
import subprocess
import threading

import bumblebee.engine
import bumblebee.input
import bumblebee.output


class Module(bumblebee.engine.Module):
    def __init__(self, engine, config):
        widget = bumblebee.output.Widget(full_text=self.get_output)
        super(Module, self).__init__(engine, config, widget)

        if self.parameter('interval'):
            self.interval(self.parameter('interval'))

        self._command = self.parameter('command')
        self._async = bumblebee.util.asbool(self.parameter('async'))
        if self._async:
            self._output = 'Computing...'
            self._current_thread = None
        else:
            self._output = ''

        # LMB and RMB will update output regardless of timer
        engine.input.register_callback(self, button=bumblebee.input.RIGHT_MOUSE, cmd=self.update)
        engine.input.register_callback(self, button=bumblebee.input.LEFT_MOUSE, cmd=self.update)

    def get_output(self, _):
        return self._output

    def update(self, _):
        # if requested then run not async version and just execute command in this thread
        if not self._async:
            self._output = self._get_command_output_or_error(self._command)
            return

        # if previous thread didn't end yet then don't do anything
        if self._current_thread:
            return

        # spawn new thread to execute command and pass callback method to get output from it
        self._current_thread = threading.Thread(target=self._run_command_in_thread,
                                                args=(self._command, self._output_function))
        self._current_thread.start()

    @staticmethod
    def _get_command_output_or_error(command):
        try:
            command_output = subprocess.check_output(command,
                                                     executable=os.environ.get('SHELL'),
                                                     shell=True,
                                                     stderr=subprocess.STDOUT)
            return command_output.decode('utf-8').strip()
        except subprocess.CalledProcessError as exception:
            exception_output = exception.output.decode('utf-8').replace('\n', '')
            return 'Status:{} output:{}'.format(exception.returncode, exception_output)

    def _run_command_in_thread(self, command, output_callback):
        output_callback(self._get_command_output_or_error(command))

    def _output_function(self, text):
        self._output = text
        # clear this thread data, so next update will spawn a new one
        self._current_thread = None

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
