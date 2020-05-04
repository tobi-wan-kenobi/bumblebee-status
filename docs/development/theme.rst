How to write a new theme
========================

Introduction
------------

``bumblebee-status`` themes are simply JSON files that describe various
attributes (foreground color, background color, etc.) of the blocks that
make up a status bar.

It is possible to specify each attribute at various levels: - For a
specific state of a specific module - For a specific module - A cycle of
attributes (those are cycled through widget-by-widget) - Default values

Looking up a value follows the “more specific rather than more generic”
approach. In other words, if a foreground color exists for the “warning”
state of module “a”, any less specific foreground color value that
**would** match will be ignored.

Themes are loaded from the following locations: -
``$(BUMBLEBEE_STATUS_BASE_DIR)/themes/`` -
``~/.config/bumblebee-status/themes/``

Basic structure
---------------

A very simple theme file looks like this:

.. code:: json

   {
       "icons": [ "awesome-fonts" ],
       "defaults": {
           "fg": "#000000",
           "bg": "#ffffff",
           "warning": {
               "fg": "#ff0000",
               "bg": "#ffffff"
           }
       }
   }

Icons
-----

Using the ``icons`` directive, it’s possible to reuse icon definitions
for multiple themes. The value of the field is the **basename** of a
JSON file located in ``$(THEME_DIRECTORY)/icons/``. The format of the
icon file is identical to the theme itself (as the two are essentially
just merged into a single JSON.

Color definitions and pyWAL support
-----------------------------------

``bumblebee-status`` supports
`github:dylanaraps/pywal <https://github.com/dylanaraps/pywal>`__
definitions.

To make use of them, simply generate a colorset using pyWAL and
reference it in the theme like this:

.. code:: json

   {
       "icons": [ ],
       "colors": [ "wal" ],
       "defaults": {
           "critical": {
               "fg": "cursor",
               "bg": "color5"
           },
           "warning": {
               "fg": "cursor",
               "bg": "color6"
           },
       } 
   }

Additionally, you can use the ``colors`` directive to set up named
colors for your scheme:

.. code:: json

   {
       "icons": [ ],
       "colors": [ { "red": "#ff0000", "green": "#00ff00", "black": "#000000" } ],
       "defaults": {
           "critical": {
               "fg": "red",
               "bg": "black"
           }
   }

Pango support
-------------

All values that accept a full text (i.e. the base level, ``prefix`` and
``suffix``) accept a special attribute ``pango`` **instead** of all
other attributes. In other words, if you specify ``pango``, any other
attribute on that level (foreground color, etc.) will be ignored!

Inside ``pango``, you can just specify arbitrary Pango attributes, and
those will be applied to a ``<span></span>`` that’s automatically
enclosing the actual text.

Full list of attributes
-----------------------

(TODO: Add explanation)

-  defaults
-  cycle
-  icons
-  warning
-  critical
-  fg
-  bg
-  separator
-  padding
-  pango
-  prefix
-  suffix
-  default-separators
-  separator-block-width
-  <module name>
-  <state>

Examples
--------

see
`github:tobi-wan-kenobi/bumblebee-status/themes <https://github.com/tobi-wan-kenobi/bumblebee-status/tree/master/themes>`__
