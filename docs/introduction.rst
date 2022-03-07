Introduction
================

Installation
----------------

.. code-block:: bash


   # from git (development snapshot)
   $ git clone git://github.com/tobi-wan-kenobi/bumblebee-status

   # from AUR:
   git clone https://aur.archlinux.org/bumblebee-status.git
   cd bumblebee-status
   makepkg -sicr

   # from PyPI (thanks @tony):
   # will install bumblebee-status into ~/.local/bin/bumblebee-status
   pip install --user bumblebee-status


There is also a SlackBuild available here: [slackbuilds:bumblebee-status](http://slackbuilds.org/repository/14.2/desktop/bumblebee-status/) - many thanks to [@Tonus1](https://github.com/Tonus1)!

Dependencies
------------

:doc:`modules` lists the dependencies
(Python modules and external executables) for each module. If you are
not using a module, you don’t need the dependencies.

Usage
------------

In your i3wm configuration, modify the *status_command* for your i3bar
like this:

.. code-block:: bash

   bar {
       status_command <path to bumblebee-status/bumblebee-status> \
           -m <list of modules> \
           -p <list of module parameters> \
           -t <theme>
   }

You can retrieve a list of modules (and their parameters) and themes by
entering:

.. code-block:: bash

   $ cd bumblebee-status
   $ ./bumblebee-status -l themes
   $ ./bumblebee-status -l modules

To change the update interval, use:

.. code-block:: bash

   $ ./bumblebee-status -m <list of modules> -p interval=<interval in seconds>

The update interval is the global "refresh" interval of the modules (i.e. how often
the bar will be updated with new data). The default interval is one second. It is
possible to use suffixes such as "m" (for minutes), or "h" for hours (e.g.
``-p interval=5m`` to update once every 5 minutes.

Note that some modules define their own intervals (e.g. most modules that query
an online service), such as to not cause a storm of "once every second" queries.

For more details on that, please refer to :doc:`features`.

All modules can be given “aliases” using ``<module name>:<alias>``, by
which they can be parametrized, for example:

.. code-block:: bash

   $ ./bumblebee-status -m disk:root disk:home -p root.path=/ home.path=/home

As a simple example, this is what my i3 configuration looks like:

.. code-block:: bash

   bar {
       font pango:Inconsolata 10
       position top
       tray_output none
       status_command ~/.i3/bumblebee-status/bumblebee-status -m nic disk:root \
           cpu memory battery date time pasink pasource dnf \
           -p root.path=/ time.format="%H:%M CW %V" date.format="%a, %b %d %Y" \
           -t solarized-powerline
   }

Restart i3wm and - that’s it!

