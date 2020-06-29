How to write a theme
========================

Introduction
------------

``bumblebee-status`` themes are simply JSON files that describe various
attributes (foreground color, background color, etc.) of the blocks that
make up a status bar.

It is possible to specify each attribute at various levels:

 - For a specific state of a specific module
 - For a specific module
 - A cycle of attributes (those are cycled through widget-by-widget)
 - Default values

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

To create an "icon-only" widget (e.g. the play/pause/forward/rewind buttons
of a media player), you need to do the following:

1. In the module, create a widget, and set its state to a descriptive value
   (for example `widget.set("state", "next")`
2. In the theme's icon definition JSON, define a `prefix` for that state:

.. code:: json

    {
      "spotify": {
        "next": { "prefix": "<next icon>" }
      },
    }

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

This list specifies the names of all attributes, their JSON type and a short description.

defaults, object
  Container to specify fallback values, in case nothing more specific matches.
  Can itself contain any of the other attributes (to e.g. specify a default background
  color).
cycle, array of objects
  Similar to defaults, but specifies a list of containers that is iterated for each
  widget being drawn. Effectively, this allows alternating attribute values for 
  widgets (for a powerline effect, for example)
icons, array of strings
  Allows loading of external JSON files and merging them into the current one (adding fields
  that do not exist in the current JSON, but not overwriting existing values). In practice, this
  is used to load common icon sets (hence the name).
warning, object
  Specifies attributes such as foreground or background colors for a widget that is in state
  "warning"
critical, object
  Specifies attributes such as foreground or background colors for a widget that is in state
  "critical"
fg, string
  Specifies foreground (text) color
bg, string
  Specifies background (block) color
separator, string
  Specifies a string that will be used as separator between two widgets
padding, string
  Specifies a string that will be used as padding at the beginning and end of each widget
pango, object
  Specifies `pango <https://developer.gnome.org/platform-overview/stable/tech-pango.html>`_ markup
  attributes. Once this attribute is encountered, all other text formatting, such as `fg` or `bg`
  are ignored for this widget!
prefix, string
  Specifies a string that will be used as prefix for matching widgets
suffix, string
  Specifies a string that will be used as suffix for matching widgets
default-separators, boolean
  If set to true, the default i3bar separators are drawn, otherwise not
separator-block-width, integer
  Specifies the width of the i3bar default separators, if they are drawn
<module name>, object
  Container to specify values matching a specific module
<state>, object
  Container to specify values matching a specific state of a widget

Note that it is also possible to nest containers, for example, it is possible to embed a "state"
object inside a specific "module" object to have formatting specific to one module, depending
on the state of a widget.

In concrete terms, this is used, for example, by multiple mediaplayer modules (cmus, deadbeef, etc.)
to have specific formatting for play/pause, etc, for that single widget only, like this:

.. code-block:: json

    {
        "cmus": {
            "playing": {
                "prefix": "play"
            }
        }
    }

Examples
--------

see
`github:tobi-wan-kenobi/bumblebee-status/themes <https://github.com/tobi-wan-kenobi/bumblebee-status/tree/main/themes>`__
