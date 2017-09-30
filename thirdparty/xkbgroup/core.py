# -*- coding: utf-8 -*-

"""
    xkbgroup.core
    ~~~~~~~~~~~~~

    This module implements the XKeyboard API.

    Classes:
    * XKeyboard: the main class.

    Exceptions:
    * X11Error: raised for errors on X server issues.

    :copyright: (c) 2016 by Nguyen Duc My.
    :license: MIT, see LICENSE for more details.
"""

import os
import re
import sys

from ctypes import *
try:
    from collections import UserList
except ImportError:
    from UserList import UserList

from collections import namedtuple

from .xkb import *


# Error-related utilities

OPEN_DISPLAY_ERRORS = {
    XkbOD_BadLibraryVersion: "{libname} uses XKB version {used_major}.{used_minor}\n"
                             "Xlib supports incompatible version {found_major}.{found_minor}",
    XkbOD_ConnectionRefused: "Cannot open display \"{display_name}\"",
    XkbOD_BadServerVersion: "{libname} uses XKB version {used_major}.{used_minor}\n"
                            "Server \"{display_name}\" uses incompatible version "
                                "{found_major}.{found_minor}",
    XkbOD_NonXkbServer: "XKB extension not present on \"{display_name}\"",
}

GET_CONTROLS_ERRORS = {
    BadAlloc: "Unable to allocate storage",
    BadImplementation: "Invalid reply from server",
    BadMatch: "A compatible version of Xkb was not available in the server or "
              "an argument has correct type and range, but is otherwise invalid",
}

GET_NAMES_ERRORS = {
    BadAlloc: "Unable to allocate storage",
    BadImplementation: "Invalid reply from server",
    BadLength: "The length of a request is shorter or longer than that "
               "required to minimally contain the arguments",
    BadMatch: "A compatible version of Xkb was not available in the server or "
              "an argument has correct type and range, but is otherwise invalid",
}

class X11Error(Exception):
    """Exception class, raised for errors on X server issues."""

def _ensure_type(obj, type):
    if not isinstance(obj, type):
        raise ValueError("Wrong value type, must be {}.".format(str(type)))


# Both Python 3.2+ compatible and more neat than assigning to __doc__
class GroupData(namedtuple("GroupData", ["num", "name", "symbol", "variant"])):
    """Contains all data about the specific group."""

    def __format__(self, format_spec):
        """If format_spec is not empty, use it as a format string in
        format_spec.format(...) with keyword arguments named corresponding to
        fields. Otherwise just return str(self).

        :param format_spec: format specifier
        :rtype: str
        """
        if len(format_spec) > 0:
            return format_spec.format(
                num=self.num,
                name=self.name,
                symbol=self.symbol,
                variant=self.variant)
        return str(self)

class XKeyboard:
    """The main class.

    Usage examples:

      # Assume we have the following configuration
      $ setxkbmap -layout us,ru,ua,fr
      $ python
      >>> from xkbgroup import XKeyboard
      >>> xkb = XKeyboard()
      >>> xkb.group_num
      1
      >>> xkb.group_num = 2
      >>> xkb.group_num
      2
      >>> xkb.group_num -= 2
      >>> xkb.group_num
      0
      >>> xkb.group_name
      English (US)
      >>> xkb.group_name = 'Ukrainian'
      >>> xkb.group_name
      Ukrainian
      >>> xkb.group_num
      2
      >>> xkb.group_symbol
      ua
      >>> xkb.group_symbol = 'fr'
      >>> xkb.group_symbol
      fr
      >>> xkb.group_variant
      ''
      >>> xkb.group_num -= 3
      >>> xkb.group_variant
      ''
      >>> xkb.group_num
      0
      >>>
    """

    # Fields with default values

    non_symbols = {"pc", "inet", "group", "terminate"}


    # Main methods

    def __init__(self, auto_open=True, non_symbols=None):
        """
        :param auto_open: if True automatically call open_display().
        :param non_symbols: either iterable of string non-symbol names or
                            None to use the default set of non-symbol names.
        """
        if non_symbols:
            self.non_symbols = non_symbols

        if auto_open:
            self.open_display()

    def open_display(self):
        """Establishes connection with X server and prepares objects
        necessary to retrieve and send data.
        """
        self.close_display()    # Properly finish previous open_display()

        XkbIgnoreExtension(False)

        display_name = None
        major = c_int(XkbMajorVersion)
        minor = c_int(XkbMinorVersion)
        reason = c_int()

        self._display = XkbOpenDisplay(
            display_name,
            None, None, byref(major), byref(minor), byref(reason))
        if not self._display:
            if reason.value in OPEN_DISPLAY_ERRORS:
                # Assume POSIX conformance
                display_name = os.getenv("DISPLAY") or "default"

                raise X11Error(OPEN_DISPLAY_ERRORS[reason.value].format(
                    libname="xkbgroup",
                    used_major=XkbMajorVersion,
                    used_minor=XkbMinorVersion,
                    found_major=major.value,
                    found_minor=minor.value,
                    display_name=display_name)
                        + ".")
            else:
                raise X11Error("Unknown error {} from XkbOpenDisplay.".format(reason.value))

        self._keyboard_description = XkbGetMap(self._display, 0, XkbUseCoreKbd)
        if not self._keyboard_description:
            self.close_display()
            raise X11Error("Failed to get keyboard description.")

        # Controls mask doesn't affect the availability of xkb->ctrls->num_groups anyway
        # Just use a valid value, and xkb->ctrls->num_groups will be definitely set
        status = XkbGetControls(self._display, XkbAllControlsMask, self._keyboard_description)
        if status != Success:
            self.close_display()
            raise X11Error(GET_CONTROLS_ERRORS[status] + ".")

        names_mask = XkbSymbolsNameMask | XkbGroupNamesMask
        status = XkbGetNames(self._display, names_mask, self._keyboard_description)
        if status != Success:
            self.close_display()
            raise X11Error(GET_NAMES_ERRORS[status] + ".")

    def close_display(self):
        """Closes connection with X server and cleans up objects
        created on open_display().
        """
        if hasattr(self, "_keyboard_description") and self._keyboard_description:
            names_mask = XkbSymbolsNameMask | XkbGroupNamesMask
            XkbFreeNames(self._keyboard_description, names_mask, True)
            XkbFreeControls(self._keyboard_description, XkbAllControlsMask, True)
            XkbFreeClientMap(self._keyboard_description, 0, True)
            del self._keyboard_description

        if hasattr(self, "_display") and self._display:
            XCloseDisplay(self._display)
            del self._display

    def __del__(self):
        self.close_display()

    def __enter__(self):
        self.open_display()
        return self

    def __exit__(self, type, value, traceback):
        self.close_display()


    # Properties for all layouts

    @property
    def groups_data(self):
        """All data about all groups (get-only).

        :getter: Returns all data about all groups
        :type: list of GroupData
        """
        return _ListProxy(GroupData(num, name, symbol, variant)
                          for (num, name, symbol, variant)
                          in zip(range(self.groups_count),
                                 self.groups_names,
                                 self.groups_symbols,
                                 self.groups_variants))

    @property
    def groups_count(self):
        """Number of all groups (get-only).

        :getter: Returns number of all groups
        :type: int
        """
        if self._keyboard_description.contents.ctrls is not None:
            return self._keyboard_description.contents.ctrls.contents.num_groups
        else:
            groups_source = self._groups_source

            groups_count = 0
            while (groups_count < XkbNumKbdGroups and
                   groups_source[groups_count] != None_):
                groups_count += 1

            return groups_count

    @property
    def groups_names(self):
        """Names of all groups (get-only).

        :getter: Returns names of all groups
        :type: list of str
        """
        return _ListProxy(self._get_group_name_by_num(i) for i in range(self.groups_count))

    @property
    def groups_symbols(self):
        """Symbols of all groups (get-only).

        :getter: Returns symbols of all groups
        :type: list of str
        """
        return _ListProxy(symdata.symbol for symdata in self._symboldata_list)

    @property
    def groups_variants(self):
        """Variants of all groups (get-only).

        :getter: Returns variants of all groups
        :type: list of str
        """
        return _ListProxy(symdata.variant or "" for symdata in self._symboldata_list)


    # Properties and methods for current layout

    @property
    def group_data(self):
        """All data about the current group (get-only).

        :getter: Returns all data about the current group
        :type: GroupData
        """
        return GroupData(self.group_num,
                         self.group_name,
                         self.group_symbol,
                         self.group_variant)

    @property
    def group_num(self):
        """Current group number.

        :getter: Returns current group number
        :setter: Sets current group number
        :type: int
        """
        xkb_state = XkbStateRec()
        XkbGetState(self._display, XkbUseCoreKbd, byref(xkb_state))
        return xkb_state.group

    @group_num.setter
    def group_num(self, value):
        _ensure_type(value, int)
        if XkbLockGroup(self._display, XkbUseCoreKbd, value):
            XFlush(self._display)
        else:
            self.close_display()
            raise X11Error("Failed to set group number.")


    @property
    def group_name(self):
        """Current group full name.

        :getter: Returns current group name
        :setter: Sets current group name
        :type: str
        """
        return self._get_group_name_by_num(self.group_num)

    @group_name.setter
    def group_name(self, value):
        _ensure_type(value, str)
        groups_names = self.groups_names
        n_mapping = {groups_names[i]: i for i in range(len(groups_names))}
        try:
            self.group_num = n_mapping[value]
        except KeyError as exc:
            raise ValueError("Wrong group name.")


    @property
    def group_symbol(self):
        """Current group symbol.

        :getter: Returns current group symbol
        :setter: Sets current group symbol
        :type: str
        """
        s_mapping = {symdata.index: symdata.symbol for symdata in self._symboldata_list}
        return s_mapping[self.group_num]

    @group_symbol.setter
    def group_symbol(self, value):
        _ensure_type(value, str)
        s_mapping = {symdata.symbol: symdata.index for symdata in self._symboldata_list}
        try:
            self.group_num = s_mapping[value]
        except KeyError as exc:
            raise ValueError("Wrong group symbol.")


    @property
    def group_variant(self):
        """Current group variant (get-only).

        :getter: Returns current group variant
        :type: str
        """
        v_mapping = {symdata.index: symdata.variant for symdata in self._symboldata_list}
        return v_mapping[self.group_num] or ""

    # Current group variant is a get-only value because variants are associated
    # with symbols in /usr/share/X11/xkb/rules/evdev.lst and specified at
    # setxkbmap call time


    # Formatting method (for the great goodness!)

    def format(self, format_str):
        """Returns a formatted version of format_str.
        The only named replacement fields supported by this method and
        their corresponding API calls are:

        * {num}           group_num
        * {name}          group_name
        * {symbol}        group_symbol
        * {variant}       group_variant
        * {current_data}  group_data
        * {nums}          groups_nums
        * {names}         groups_names
        * {symbols}       groups_symbols
        * {variants}      groups_variants
        * {all_data}      groups_data

        Passing other replacement fields will result in raising exceptions.

        :param format_str: a new style format string
        :rtype: str
        """
        return format_str.format(**{
            "num": self.group_num,
            "name": self.group_name,
            "symbol": self.group_symbol,
            "variant": self.group_variant,
            "current_data": self.group_data,
            "count": self.groups_count,
            "names": self.groups_names,
            "symbols": self.groups_symbols,
            "variants": self.groups_variants,
            "all_data": self.groups_data})

    def __format__(self, format_spec):
        """Handle format(xkb, format_spec) as xkb.format(format_spec) if
        format_spec is not empty. Otherwise just return str(self).

        :param format_spec: format specifier
        :rtype: str
        """
        if len(format_spec) > 0:
            return self.format(format_spec)
        return str(self)


    # Private properties and methods

    @property
    def _groups_source(self):
        return self._keyboard_description.contents.names.contents.groups

    @property
    def _symbols_source(self):
        return self._keyboard_description.contents.names.contents.symbols

    @property
    def _symboldata_list(self):
        symbol_str_atom = self._symbols_source
        if symbol_str_atom != None_:
            b_symbol_str = XGetAtomName(self._display, symbol_str_atom)
            return _parse_symbols(b_symbol_str.decode(), self.non_symbols)
        else:
            raise X11Error("Failed to get symbol names.")

    def _get_group_name_by_num(self, group_num):
        cur_group_atom = self._groups_source[group_num]
        if cur_group_atom != None_:
            b_group_name = XGetAtomName(self._display, cur_group_atom)
            return b_group_name.decode() if b_group_name else ""
        else:
            raise X11Error("Failed to get group name.")


SymbolData = namedtuple("SymbolData", ["symbol", "variant", "index"])
SYMBOL_REGEX = re.compile(r"""
    (?P<symbol>\w+)
    (?: \( (?P<variant>\w+) \) )?
    (?: : (?P<index>\d+) )?
    """, re.VERBOSE)

class _Compat_SRE_Pattern:
    def __init__(self, re_obj):
        self.re_obj = re_obj

    def __getattr__(self, name):
        return getattr(self.re_obj, name)

    # re_obj.fullmatch is a Python 3.4+ only feature
    def fullmatch(self, string, pos=None, endpos=None):
        pos = pos if pos else 0
        endpos = endpos if endpos else len(string)
        match = self.re_obj.match(string, pos, endpos)
        if match and match.span() != (pos, endpos):
            return None
        return match

if sys.version_info < (3, 4):
    SYMBOL_REGEX = _Compat_SRE_Pattern(SYMBOL_REGEX)

def _parse_symbols(symbols_str, non_symbols, default_index=0):
    def get_symboldata(symstr):
        match = SYMBOL_REGEX.fullmatch(symstr)
        if match:
            index = match.group('index')
            return SymbolData(
                match.group('symbol'),
                match.group('variant'),
                int(index) - 1 if index else default_index)
        else:
            raise X11Error("Malformed symbol string: \"{}\"".format(symstr))

    symboldata_list = []
    for symstr in symbols_str.split('+'):
        symboldata = get_symboldata(symstr)
        if symboldata.symbol not in non_symbols:
            symboldata_list.append(symboldata)

    indices = [symdata.index for symdata in symboldata_list]
    assert len(indices) == len(set(indices))    # No doubles

    return symboldata_list


_COLON_SEPARATOR_REGEX = re.compile(r"(?<!\\):")

class _ListProxy(UserList):
    def __format__(self, format_spec):
        if len(format_spec) > 0:
            spec_parts = _COLON_SEPARATOR_REGEX.split(format_spec)
            spec_parts = [s.replace("\\:", ":") for s in spec_parts]
            assert len(spec_parts) > 0

            elem_spec = spec_parts[0]
            elems_formatted = [format(x, elem_spec) for x in self.data]

            if len(spec_parts) == 1:
                assert len(elem_spec) > 0
                return str(elems_formatted)
            elif len(spec_parts) == 2:
                sep = spec_parts[1]
                return sep.join(elems_formatted)
            else:
                raise ValueError(
                    "Too many specifiers: \"{}\"".format(format_spec))

        return str(self.data)


__all__ = ["XKeyboard", "GroupData", "X11Error"]


def print_xkeyboard(xkb):
    print("xkb {")
    contents = [
        "%d groups {%s}," % (xkb.groups_count, ", ".join(xkb.groups_names)),
        "symbols {%s}" % ", ".join(xkb.groups_symbols),
        "variants {%s}" % ", ".join('"{}"'.format(variant) for variant in xkb.groups_variants),
        "current group: %s (%d) - %s - \"%s\"" %
            (xkb.group_symbol, xkb.group_num, xkb.group_name, xkb.group_variant)
    ]
    print("\n".join("\t" + line for line in contents))
    print("}")

def test():
    with XKeyboard() as xkb:
        print_xkeyboard(xkb)
        xkb.group_num += 2
        print_xkeyboard(xkb)
        xkb.group_num -= 3
        print_xkeyboard(xkb)
        xkb.group_num -= 2
        print_xkeyboard(xkb)

if __name__ == '__main__':
    test()
