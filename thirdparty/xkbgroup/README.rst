========
xkbgroup
========

.. image:: https://img.shields.io/badge/python-3.2+-blue.svg

.. image:: https://img.shields.io/pypi/v/xkbgroup.svg
    :target: https://pypi.python.org/pypi/xkbgroup

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/hcpl/xkbgroup/blob/master/LICENSE

Use this library to change the keyboard layout through XKB extension (subsystem)
of the X server system. Both library and command line script included.


.. contents:: **Table of Contents**


Dependencies
------------

* Python 3.2+
* ``libX11.so.6`` shared library which you must have by default if you use
  X server


Installation
------------

From PyPI package xkbgroup__
++++++++++++++++++++++++++++

__ https://pypi.python.org/pypi/xkbgroup

.. code-block:: sh

    pip install xkbgroup


Library usage
-------------

.. code-block:: sh

   # Assume we have the following configuration
   $ setxkbmap -layout us,ru,ua,fr
   # Change layout once before calling python
   $ python

.. code-block:: python

   >>> from xkbgroup import XKeyboard
   >>> xkb = XKeyboard()
   >>> xkb.groups_count
   4
   >>> xkb.group_num
   1
   >>> xkb.group_num = 2
   >>> xkb.group_num
   2
   >>> xkb.group_num -= 2
   >>> xkb.group_num
   0
   >>> xkb.groups_names
   ['English (US)', 'Russian', 'Ukrainian', 'French']
   >>> xkb.group_name
   'English (US)'
   >>> xkb.group_name = 'Ukrainian'
   >>> xkb.group_name
   'Ukrainian'
   >>> xkb.group_num
   2
   >>> xkb.groups_symbols
   ['us', 'ru', 'ua', 'fr']
   >>> xkb.group_symbol
   'ua'
   >>> xkb.group_symbol = 'fr'
   >>> xkb.group_symbol
   'fr'
   >>> xkb.groups_variants
   ['', '', '', '']
   >>> xkb.group_variant
   ''
   >>> xkb.group_num -= 3
   >>> xkb.group_variant
   ''
   >>> xkb.group_num
   0
   >>> xkb.group_data
   GroupData(num=0, name='English (US)', symbol='us', variant='')
   >>> xkb.groups_data
   [GroupData(num=0, name='English (US)', symbol='us', variant=''), GroupData(num=1, name=
   'Russian', symbol='ru', variant=''), GroupData(num=2, name='Ukrainian', symbol='ua', va
   riant=''), GroupData(num=3, name='French', symbol='fr', variant='')]
   >>> xkb.format('{num} => {symbol}')
   '0 => us'
   >>> xkb.group_num = 1
   >>> xkb.format('{num} => {symbol}')
   '1 => ru'
   >>> xkb.group_num = 3
   >>> xkb.format('{num}: {symbol} - {name} "{variant}"')
   '3: fr - French ""'
   >>> xkb.format('{count}')
   '4'
   >>> xkb.format('{names}')
   "['English (US)', 'Russian', 'Ukrainian', 'French']"
   >>> xkb.format('{names::}')
   'English (US)RussianUkrainianFrench'
   >>> xkb.format('{names:: - }')
   'English (US) - Russian - Ukrainian - French'
   >>> xkb.format('{symbols:: - }')
   'us - ru - ua - fr'
   >>> xkb.format('{symbols:s: - }')
   'us - ru - ua - fr'
   >>> xkb.format('{all_data}')
   "[GroupData(num=0, name='English (US)', symbol='us', variant=''), GroupData(num=1, name
   ='Russian', symbol='ru', variant=''), GroupData(num=2, name='Ukrainian', symbol='ua', v
   ariant=''), GroupData(num=3, name='French', symbol='fr', variant='')]"
   >>> xkb.format('{all_data:{{num}}}')
   "['0', '1', '2', '3']"
   >>> xkb.format('{all_data:/* {{name}} */}')
   "['/* English (US) */', '/* Russian */', '/* Ukrainian */', '/* French */']"
   >>> xkb.format('{all_data:{{symbol}}:\n}')
   'us\nru\nua\nfr'
   >>> print(xkb.format('{all_data:{{symbol}}:\n}'))
   us
   ru
   ua
   fr
   >>> print(xkb.format('{all_data:{{num}}\\: {{symbol}} - {{name}} - "{{variant}}":\n}'))
   0: us - English (US) - ""
   1: ru - Russian - ""
   2: ua - Ukrainian - ""
   3: fr - French - ""
   >>>


Command line features mapping
-----------------------------

+----------+-------------------------------------+--------------------------------------+
| Category |               Library               |            Command line              |
+==========+=====================================+======================================+
| Get      | ``xkb.group_num``                   | ``xkbgroup get num``                 |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_name``                  | ``xkbgroup get name``                |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_symbol``                | ``xkbgroup get symbol``              |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_variant``               | ``xkbgroup get variant``             |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_data``                  | ``xkbgroup get current_data``        |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.groups_count``                | ``xkbgroup get count``               |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.groups_names``                | ``xkbgroup get names``               |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.groups_symbols``              | ``xkbgroup get symbols``             |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.groups_variants``             | ``xkbgroup get variants``            |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.groups_data``                 | ``xkbgroup get all_data``            |
+----------+-------------------------------------+--------------------------------------+
| Set      | ``xkb.group_num = 2``               | ``xkbgroup set num 2``               |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_name = 'English (US)'`` | ``xkbgroup set name 'English (US)'`` |
|          +-------------------------------------+--------------------------------------+
|          | ``xkb.group_symbol = 'fr'``         | ``xkbgroup set symbol fr``           |
+----------+-------------------------------------+--------------------------------------+
| Format   | ``xkb.format('{format_str}')``      | ``xkbgroup format '{format_str}'``   |
+----------+-------------------------------------+--------------------------------------+


Naming convention
-----------------

Throughout the whole XKB subsystem the `so-called groups represent actual
keyboard layouts`__. This library follows the same convention and names of the
API methods start with ``group_`` or ``groups_``.

__ https://wiki.archlinux.org/index.php/X_KeyBoard_extension#Keycode_translation


Classes
-------

These all reside in ``xkbgroup/core.py``:

* ``XKeyboard`` — the main class:

  - ``__init__(self, auto_open=True, non_symbols=None)``:

    + ``auto_open`` — if ``True`` then automatically call ``open_display()``
      on initialization.
    + ``non_symbols`` — either iterable of string non-symbol names or None to
      use the default set of non-symbol names.
  - ``open_display()`` — establishes connection with X server and prepares
    objects necessary to retrieve and send data.
  - ``close_display()`` — closes connection with X server and cleans up
    objects created on ``open_display()``.
  - ``group_*`` — properties for accessing current group data:

    + ``group_num`` — get/set current group number
      (e.g. ``0``, ``2``, ``3``).
    + ``group_name`` — get/set current group full name
      (e.g. ``English (US)``, ``Russian``, ``French``).
    + ``group_symbol`` — get/set current group symbol
      (e.g. ``us``, ``ru``, ``fr``).
    + ``group_variant`` — get (only) current group variant
      (e.g. `` ``, ``dos``, ``latin9``).
    + ``group_data`` — get (only) all data about the current group.
      In fact, assembles all previous ``group_*`` values.
  - ``groups_*`` — properties for querying info about all groups set by
    ``setxkbmap``:

    + ``groups_count`` — get number of all groups.
    + ``groups_names`` — get names of all groups.
    + ``groups_symbols`` — get symbols of all groups.
    + ``groups_variants`` — get variants of all groups.
    + ``groups_data`` — get all data about all groups
      by assembling all previous ``groups_*`` values.

  - ``format()`` — obtain a formatted output, see `<docs/formatting.rst>`_
    for details.

* ``X11Error`` — an exception class, raised for errors on X server issues.


Helper files
------------

There are also complementary files:

* ``generate_bindings.sh`` — a shell script which generates Python bindings
  to X server structures, functions and ``#define`` definitions by:

  - converting X11 C headers using ``h2xml`` and ``xml2py``;
  - creating ``ctypes`` references to functions from ``libX11.so.6`` using
    ``xml2py``.

* ``xkbgroup/xkb.py`` — the output of the above script, usable for Xlib
  development under Python.
