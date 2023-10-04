# pylint: disable=C0111,R0903
"""
Displays the current Power-Profile active


Left-Click or Right-Click as well as Scrolling up / down changes the active Power-Profile

Prerequisites:
    * dbus-python
    * power-profiles-daemon
"""

import dbus
import core.module
import core.widget
import core.input


class PowerProfileManager:
    def __init__(self):
        self.POWER_PROFILES_NAME = "net.hadess.PowerProfiles"
        self.POWER_PROFILES_PATH = "/net/hadess/PowerProfiles"
        self.PP_PROPERTIES_CURRENT_POWER_PROFILE = "ActiveProfile"
        self.PP_PROPERTIES_ALL_POWER_PROFILES = "Profiles"

        self.DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
        bus = dbus.SystemBus()
        pp_proxy = bus.get_object(self.POWER_PROFILES_NAME, self.POWER_PROFILES_PATH)
        self.pp_interface = dbus.Interface(pp_proxy, self.DBUS_PROPERTIES)

    def get_current_power_profile(self):
        return self.pp_interface.Get(
            self.POWER_PROFILES_NAME, self.PP_PROPERTIES_CURRENT_POWER_PROFILE
        )

    def __get_all_power_profile_names(self):
        power_profiles = self.pp_interface.Get(
            self.POWER_PROFILES_NAME, self.PP_PROPERTIES_ALL_POWER_PROFILES
        )
        power_profiles_names = []
        for pp in power_profiles:
            power_profiles_names.append(pp["Profile"])

        return power_profiles_names

    def next_power_profile(self, event):
        all_pp_names = self.__get_all_power_profile_names()
        current_pp_index = self.__get_current_pp_index()
        next_index = 0
        if current_pp_index != (len(all_pp_names) - 1):
            next_index = current_pp_index + 1

        self.pp_interface.Set(
            self.POWER_PROFILES_NAME,
            self.PP_PROPERTIES_CURRENT_POWER_PROFILE,
            all_pp_names[next_index],
        )

    def prev_power_profile(self, event):
        all_pp_names = self.__get_all_power_profile_names()
        current_pp_index = self.__get_current_pp_index()
        last_index = len(all_pp_names) - 1
        if current_pp_index is not 0:
            last_index = current_pp_index - 1

        self.pp_interface.Set(
            self.POWER_PROFILES_NAME,
            self.PP_PROPERTIES_CURRENT_POWER_PROFILE,
            all_pp_names[last_index],
        )

    def __get_current_pp_index(self):
        all_pp_names = self.__get_all_power_profile_names()
        current_pp = self.get_current_power_profile()
        return all_pp_names.index(current_pp)


class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.full_text))
        self.pp_manager = PowerProfileManager()
        core.input.register(
            self, button=core.input.WHEEL_UP, cmd=self.pp_manager.next_power_profile
        )
        core.input.register(
            self, button=core.input.WHEEL_DOWN, cmd=self.pp_manager.prev_power_profile
        )
        core.input.register(
            self, button=core.input.LEFT_MOUSE, cmd=self.pp_manager.next_power_profile
        )
        core.input.register(
            self, button=core.input.RIGHT_MOUSE, cmd=self.pp_manager.prev_power_profile
        )

    def full_text(self, widgets):
        return self.pp_manager.get_current_power_profile()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
