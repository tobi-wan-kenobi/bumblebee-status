Advanced usage
===========================

Intervals
---------

Some modules define their own update intervals (e.g. most modules that query
an online service), such as to not cause a storm of "once every second" queries.

For such modules, the "global" interval defined via the ``interval`` parameter effectively defines the
highest possible "resolution". If you have a global interval of 10s, for example,
any other module can update at 10s, 20s, 30s, etc., but not every 25s. The status
bar will internally always align to the next future time slot.

The update interval can also be changed on a per-module basis, like
this (overriding the default module interval indicated above):

.. code-block:: bash

   $ ./bumblebee-status -m cpu memory -p cpu.interval=5s memory.interval=1m


Events
------

Many modules provide default handling for various events, for example:

-  Mouse-Wheel on any module moves to the next/previous i3 workspace
-  Left-click on the “disk” module opens the specified path in a file
   browser
-  Left-click on either “memory” or “cpu” opens a system monitor
-  Left-click on a “pulseaudio” (or pasource/pasink) module toggles the
   mute state
-  Mouse-Wheel up/down on a “pulseaudio” module raises/lowers the volume

You can provide your own handlers to any module by using the following
“special” configuration parameters:

-  left-click
-  right-click
-  middle-click
-  wheel-up
-  wheel-down

For example, to execute “pavucontrol” whenever you
left-click on the nic module, you could write:

``$ bumblebee-status -p nic.left-click="pavucontrol"``

In the string, you can use the following format identifiers: - name -
instance - button

For example:

``$ bumblebee-status -p disk.left-click="nautilus {instance}"``

Update intervals
----------------

The general “update interval” is set using the ``-i|--interval``
parameter of ``bumblebee-status``, and defaults to 1 second. Some
modules override this interval to update less frequently (e.g. the
kernel version is updated only very rarely, as it usually doesn’t change
during runtime). Also, modules like ``weather`` or ``stock`` update less
frequently, to avoid hitting API limits.

For each module, it is possible to specify a parameter ``interval`` to
override that behaviour.

For example, to update the battery status once per minute, you’d use
something like this:

``$ bumblebee-status -m battery -p battery.interval=1m``

The format supports: - numbers (assumed to be seconds -
``battery.interval=20`` means every 20s) - ``h``, ``m``, ``s`` and
combinations thereof - ``battery.interval=2m30s`` means every 2 minutes,
30 seconds)

Errors
------

If errors occur, you should see them in the i3bar itself. If that does
not work, or you need more information for troubleshooting, you can
activate a debug log using the ``-d`` or ``--debug`` switch:

::

   $ ./bumblebee-status -d -m <list of modules>

This will log to stderr, so unless you are running ``bumblebee-status``
interactively in the CLI, you’ll need to specify a logfile using ``-f``
or ``--logfile``. Note that putting ``bumblebee-status`` into debug mode
will show an indicator in the bar to make sure you don’t forget to clean
up the log file occasionally.

Automatically hiding modules
----------------------------

If you want to have a minimal bar that stays out of the way, you can use
the ``-a`` or ``--autohide`` switch to specify a list of module names.
All those modules will only be displayed when (and as long as) their
state is either warning or critical (high CPU usage, low disk space,
etc.). As long as the module is in a “normal” state and does not require
attention, it will remain hidden. Note that this parameter is specified
*in addition* to ``-m`` (i.e. to autohide the CPU module, you would use
``bumblebee-status -m cpu memory traffic -a cpu``).

Scrolling widget text
-----------------------
Some widgets support scrolling for long text (e.g. most music player
widgets, rss, etc.). Those have some additional settings for customizing
the scrolling behaviour, in particular:

  - ``scrolling.width``: Desired width of the scrolling panel
  - ``scrolling.makewide``: If set to true, extends texts shorter than
    ``scrolling.width`` to that width
  - ``scrolling.bounce``: If set to true, bounces the text when it reaches
    the end, otherwise, it behaves like marquee (scroll-through) text
  - ``scrolling.speed``: Defines the scroll speed, in characters per update

Additional widget theme settings
--------------------------------

There are a few parameters you can tweak directly from the commandline
via ``-p`` or ``--parameters``: - ``<modulename>.theme.minwidth`` sets
the minimum width of a module/widget (can be a comma-separated list for
multi-widget modules). The parameter can be either an integer (in which
case it is taken as “number of characters”, or a string, in which case
the minwidth is the width of the string
(e.g. ``-p cpu.minwidth="100.00%"``) - ``<modulename>.theme.align`` sets
the alignment (again, can be comma-separated for multi-widget modules) -
defaults to ``left``, valid values are ``left``, ``right`` and
``center``

An example:

::

   $ bumblebee-status -m sensors2 -p sensors2.theme.minwidth=10,10,10,10 sensors2.theme.align=center,center,left,right

Configuration files
-------------------

Using a configuration file, it is possible to define a list of modules
that will be loaded if no modules are specified on the CLI, as well as
defining a default theme to use.

Any parameter that can be specified using ``-p <name>=<value>`` on the
commandline, can alternatively be specified in one of the following
configuration files: - ~/.bumblebee-status.conf -
~/.config/bumblebee-status.conf - ~/.config/bumblebee-status/config

These parameters act as **fallback**, so values specified on the
commandline take precedence.

Configuration files have the following format:

::

   [core]
   modules = <comma-separated list of modules to load>
   autohide = <comma-separated list of modules to hide, unless in warning/error state>
   theme = <theme to use by default>

   [module-parameters]
   <key> = <value>

For example:

::

   [module-parameters]
   github.token=abcdefabcdef12345


