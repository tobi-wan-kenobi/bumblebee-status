"""Core application engine"""

import os
import json
import time
import pkgutil
import logging
import importlib
import bumblebee.error
import bumblebee.modules

log = logging.getLogger(__name__)

try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

def all_modules():
    """Return a list of available modules"""
    result = []
    path = os.path.dirname(bumblebee.modules.__file__)
    for mod in [name for _, name, _ in pkgutil.iter_modules([path])]:
        result.append({
            "name": mod
        })
    return result

class Module(object):
    """Module instance base class

    Objects of this type represent the modules that
    the user configures. Concrete module implementations
    (e.g. CPU utilization, disk usage, etc.) derive from
    this base class.
    """
    def __init__(self, engine, config={}, widgets=[]):
        self.name = config.get("name", self.__module__.split(".")[-1])
        self._config = config
        self.id = self.name
        self.error = None
        self._next = int(time.time())
        self._default_interval = 0

        self._configFile = None
        for cfg in [os.path.expanduser("~/.bumblebee-status.conf"), os.path.expanduser("~/.config/bumblebee-status.conf")]:
            if os.path.exists(cfg):
                self._configFile = RawConfigParser()
                self._configFile.read(cfg)
                log.debug("reading configuration file {}".format(cfg))
                break

        if self._configFile is not None and self._configFile.has_section("module-parameters"):
            log.debug(self._configFile.items("module-parameters"))
        self._widgets = []
        if widgets:
            self._widgets = widgets if isinstance(widgets, list) else [widgets]

    def widgets(self, widgets=None):
        """Return the widgets to draw for this module"""
        if widgets:
            self._widgets = widgets
        return self._widgets

    def hidden(self):
        return False

    def widget(self, name):
        for widget in self._widgets:
            if widget.name == name:
                return widget

    def errorWidget(self):
        msg = self.error
        if len(msg) > 10:
            msg = "{}...".format(msg[0:7])
        return bumblebee.output.Widget(full_text="error: {}".format(msg))

    def widget_by_id(self, uid):
        for widget in self._widgets:
            if widget.id == uid:
                return widget
        return None

    def update(self, widgets):
        """By default, update() is a NOP"""
        pass

    def update_wrapper(self, widgets):
        if self._next > int(time.time()):
            return
        try:
            self.error = None
            self.update(self._widgets)
        except Exception as e:
            log.error("error updating '{}': {}".format(self.name, str(e)))
            self.error = str(e)
        self._next += int(self.parameter("interval", self._default_interval))*60

    def interval(self, intvl):
        self._default_interval = intvl
        self._next = int(time.time())

    def update_all(self):
        self.update_wrapper(self._widgets)

    def has_parameter(self, name):
        v = self.parameter(name)
        return v is not None

    def parameter(self, name, default=None):
        """Return the config parameter 'name' for this module"""
        name = "{}.{}".format(self.name, name)
        value = self._config["config"].get(name, default)
        if value == default:
            try:
                value = self._configFile.get("module-parameters", name)
            except:
                pass
        return value

    def threshold_state(self, value, warn, crit):
        if value > float(self.parameter("critical", crit)):
            return "critical"
        if value > float(self.parameter("warning", warn)):
            return "warning"
        return None

class Engine(object):
    """Engine for driving the application

    This class connects input/output, instantiates all
    required modules and drives the "event loop"
    """
    def __init__(self, config, output=None, inp=None, theme=None):
        self._output = output
        self._config = config
        self._running = True
        self._modules = []
        self.input = inp
        self._aliases = self._read_aliases()
        self.load_modules(config.modules())
        self._current_module = None
        self._theme = theme

        if bumblebee.util.asbool(config.get("engine.workspacewheel", "true")):
            if bumblebee.util.asbool(config.get("engine.workspacewrap", "true")):
                self.input.register_callback(None, bumblebee.input.WHEEL_UP,
                    "i3-msg workspace prev_on_output")
                self.input.register_callback(None, bumblebee.input.WHEEL_DOWN,
                    "i3-msg workspace next_on_output")
            else:
                self.input.register_callback(None, bumblebee.input.WHEEL_UP,
                    cmd=self._prev_workspace)
                self.input.register_callback(None, bumblebee.input.WHEEL_DOWN,
                    cmd=self._next_workspace)
        if bumblebee.util.asbool(config.get("engine.collapsible", "true")):
            self.input.register_callback(None, bumblebee.input.MIDDLE_MOUSE,
                cmd=self._toggle_minimize)

        self.input.start()

    def _toggle_minimize(self, event):
        for module in self._modules:
            widget = module.widget_by_id(event["instance"])
            if widget:
                log.debug("module {} found - toggle minimize".format(module.id))
                widget.toggle_minimize()

    def _prev_workspace(self, event):
        self._change_workspace(-1)

    def _next_workspace(self, event):
        self._change_workspace(1)

    def _change_workspace(self, amount):
        try:
            active_output = None
            active_index = -1
            output_workspaces = {}
            data = json.loads(bumblebee.util.execute("i3-msg -t get_workspaces"))
            for workspace in data:
                output_workspaces.setdefault(workspace["output"], []).append(workspace)
                if workspace["focused"]:
                    active_output = workspace["output"]
                    active_index = len(output_workspaces[workspace["output"]]) - 1
            if (active_index + amount) < 0:
                return
            if (active_index + amount) >= len(output_workspaces[active_output]):
                return

            while amount != 0:
                if amount > 0:
                    bumblebee.util.execute("i3-msg workspace next_on_output")
                    amount = amount - 1
                if amount < 0:
                    bumblebee.util.execute("i3-msg workspace prev_on_output")
                    amount = amount + 1
        except Exception as e:
            log.error("failed to change workspace: {}".format(e))

    def modules(self):
        return self._modules

    def load_modules(self, modules):
        """Load specified modules and return them as list"""
        for module in modules:
            mod = self._load_module(module["module"], module["name"])
            self._modules.append(mod)
            self._register_module_callbacks(mod)
        return self._modules

    def _register_module_callbacks(self, module):
        buttons = [
            {"name": "left-click", "id": bumblebee.input.LEFT_MOUSE},
            {"name": "middle-click", "id": bumblebee.input.MIDDLE_MOUSE},
            {"name": "right-click", "id": bumblebee.input.RIGHT_MOUSE},
            {"name": "wheel-up", "id": bumblebee.input.WHEEL_UP},
            {"name": "wheel-down", "id": bumblebee.input.WHEEL_DOWN},
        ]
        for button in buttons:
            if module.parameter(button["name"], None):
                self.input.register_callback(obj=module,
                    button=button["id"], cmd=module.parameter(button["name"]))

    def _read_aliases(self):
        result = {}
        for module in all_modules():
            try:
                mod = importlib.import_module("bumblebee.modules.{}".format(module["name"]))
                for alias in getattr(mod, "ALIASES", []):
                    result[alias] = module["name"]
            except Exception as error:
                log.warning("failed to import {}: {}".format(module["name"], str(error)))
        return result

    def _load_module(self, module_name, config_name=None):
        """Load specified module and return it as object"""
        if module_name in self._aliases:
            config_name is config_name if config_name else module_name
            module_name = self._aliases[module_name]
        if config_name is None:
            config_name = module_name
        err = None
        try:
            module = importlib.import_module("bumblebee.modules.{}".format(module_name))
        except ImportError as error:
            err = error
            log.fatal("failed to import {}: {}".format(module_name, str(error)))
        if err:
            raise bumblebee.error.ModuleLoadError("unable to load module {}: {}".format(module_name, str(err)))
        return getattr(module, "Module")(self, {
            "name": config_name,
            "config": self._config
        })

    def running(self):
        """Check whether the event loop is running"""
        return self._running

    def stop(self):
        """Stop the event loop"""
        self._running = False

    def current_module(self):
        return self._current_module.__module__

    def run(self):
        """Start the event loop"""
        self._output.start()
        while self.running():
            self.write_output()
            if self.running():
                self.input.wait(float(self._config.get("interval", 1)))

        self._output.stop()
        self.input.stop()

    def write_output(self):
        self._output.begin()
        for module in self._modules:
            self._current_module = module
            module.update_wrapper(module.widgets())
            if module.error is None:
                for widget in module.widgets():
                    widget.link_module(module)
                    self._output.draw(widget=widget, module=module, engine=self)
            else:
                self._output.draw(widget=module.errorWidget(), module=module, engine=self)
        self._output.flush()
        self._output.end()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
